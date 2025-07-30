"""
RAG Service for document processing and retrieval-augmented generation
Supports multiple vector databases and document types
"""

import os
import logging
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
import json
import hashlib
import datetime

# Document processing with graceful imports
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("Warning: PyPDF2 not available - PDF processing disabled")

try:
    from docx import Document as DocxDocument
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False
    print("Warning: python-docx not available - DOCX processing disabled")

from bs4 import BeautifulSoup

# Vector databases with graceful imports
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    print("Warning: ChromaDB not available - vector storage disabled")

try:
    import pinecone
    PINECONE_AVAILABLE = True
except ImportError:
    PINECONE_AVAILABLE = False

try:
    import faiss
    import numpy as np
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    np = None

# Text processing with graceful imports
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("Warning: sentence-transformers not available - embeddings disabled")

try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False
    print("Warning: tiktoken not available - using simple token counting")

try:
    from config import Config
except ImportError:
    # Fallback config
    class Config:
        CHROMA_PERSIST_DIRECTORY = "./data/chroma"
        CHUNK_SIZE = 1000
        CHUNK_OVERLAP = 200
        TOP_K_RESULTS = 5
        SIMILARITY_THRESHOLD = 0.7
    print("Warning: Could not import config, using fallback settings")

from services.llm_service import llm_service

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Handles document processing and chunking"""
    
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or Config.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or Config.CHUNK_OVERLAP
        
        # Initialize tiktoken encoding if available
        if TIKTOKEN_AVAILABLE:
            self.encoding = tiktoken.get_encoding("cl100k_base")
        else:
            self.encoding = None
    
    def process_file(self, file_path: str) -> Dict[str, Any]:
        """Process a file and extract text content"""
        file_path = Path(file_path)
        file_extension = file_path.suffix.lower()
        
        try:
            if file_extension == '.pdf':
                text = self._extract_pdf_text(file_path)
            elif file_extension in ['.docx', '.doc']:
                text = self._extract_docx_text(file_path)
            elif file_extension == '.txt':
                text = self._extract_txt_text(file_path)
            elif file_extension == '.html':
                text = self._extract_html_text(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
            
            # Generate document metadata
            doc_hash = hashlib.md5(text.encode()).hexdigest()
            metadata = {
                "file_path": str(file_path),
                "file_name": file_path.name,
                "file_type": file_extension,
                "file_size": file_path.stat().st_size,
                "document_hash": doc_hash,
                "processed_at": str(datetime.datetime.now())
            }
            
            # Split into chunks
            chunks = self._create_chunks(text)
            
            return {
                "text": text,
                "chunks": chunks,
                "metadata": metadata,
                "chunk_count": len(chunks)
            }
            
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            raise
    
    def _extract_pdf_text(self, file_path: Path) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            logger.error(f"Error extracting PDF text: {e}")
            raise
        return text.strip()
    
    def _extract_docx_text(self, file_path: Path) -> str:
        """Extract text from DOCX file"""
        try:
            doc = DocxDocument(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            logger.error(f"Error extracting DOCX text: {e}")
            raise
        return text.strip()
    
    def _extract_txt_text(self, file_path: Path) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        except Exception as e:
            logger.error(f"Error extracting TXT text: {e}")
            raise
        return text.strip()
    
    def _extract_html_text(self, file_path: Path) -> str:
        """Extract text from HTML file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file.read(), 'html.parser')
                text = soup.get_text()
        except Exception as e:
            logger.error(f"Error extracting HTML text: {e}")
            raise
        return text.strip()
    
    def _create_chunks(self, text: str) -> List[Dict[str, Any]]:
        """Split text into chunks with overlap"""
        chunks = []
        
        if TIKTOKEN_AVAILABLE and self.encoding:
            # Use tiktoken for accurate token counting
            tokens = self.encoding.encode(text)
            
            start = 0
            while start < len(tokens):
                end = min(start + self.chunk_size, len(tokens))
                chunk_tokens = tokens[start:end]
                chunk_text = self.encoding.decode(chunk_tokens)
                
                chunks.append({
                    "text": chunk_text,
                    "start_token": start,
                    "end_token": end,
                    "token_count": len(chunk_tokens),
                    "chunk_index": len(chunks)
                })
                
                start += self.chunk_size - self.chunk_overlap
        else:
            # Simple character-based chunking as fallback
            char_per_token = 4  # Rough estimate
            chunk_size_chars = self.chunk_size * char_per_token
            overlap_chars = self.chunk_overlap * char_per_token
            
            start = 0
            while start < len(text):
                end = min(start + chunk_size_chars, len(text))
                chunk_text = text[start:end]
                
                chunks.append({
                    "text": chunk_text,
                    "start_char": start,
                    "end_char": end,
                    "token_count": len(chunk_text) // char_per_token,
                    "chunk_index": len(chunks)
                })
                
                start += chunk_size_chars - overlap_chars
        
        return chunks

class VectorStore:
    """Base class for vector stores"""
    
    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2"):
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            self.embedding_model = SentenceTransformer(embedding_model)
        else:
            self.embedding_model = None
    
    def add_documents(self, chunks: List[Dict[str, Any]], metadata: Dict[str, Any]) -> bool:
        raise NotImplementedError
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        raise NotImplementedError
    
    def delete_document(self, document_id: str) -> bool:
        raise NotImplementedError

class ChromaVectorStore(VectorStore):
    """ChromaDB vector store implementation"""
    
    def __init__(self, collection_name: str = "rag_documents", **kwargs):
        super().__init__(**kwargs)
        
        if not CHROMADB_AVAILABLE:
            raise ImportError("ChromaDB not installed. Install with: pip install chromadb")
        
        self.client = chromadb.PersistentClient(path=Config.CHROMA_PERSIST_DIRECTORY)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_documents(self, chunks: List[Dict[str, Any]], metadata: Dict[str, Any]) -> bool:
        try:
            if not SENTENCE_TRANSFORMERS_AVAILABLE or not self.embedding_model:
                logger.warning("Embeddings not available - cannot add documents")
                return False
                
            documents = [chunk["text"] for chunk in chunks]
            embeddings = self.embedding_model.encode(documents).tolist()
            
            ids = [f"{metadata['document_hash']}_{chunk['chunk_index']}" for chunk in chunks]
            metadatas = []
            
            for chunk in chunks:
                chunk_metadata = {
                    **metadata,
                    "chunk_index": chunk["chunk_index"],
                    "token_count": chunk["token_count"],
                    "start_token": chunk["start_token"],
                    "end_token": chunk["end_token"]
                }
                metadatas.append(chunk_metadata)
            
            self.collection.add(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Added {len(chunks)} chunks to ChromaDB")
            return True
            
        except Exception as e:
            logger.error(f"Error adding documents to ChromaDB: {e}")
            return False
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        try:
            if not SENTENCE_TRANSFORMERS_AVAILABLE or not self.embedding_model:
                logger.warning("Embeddings not available - cannot search")
                return []
                
            query_embedding = self.embedding_model.encode([query]).tolist()
            
            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=top_k,
                include=["documents", "metadatas", "distances"]
            )
            
            formatted_results = []
            if results["documents"]:
                for i, doc in enumerate(results["documents"][0]):
                    formatted_results.append({
                        "text": doc,
                        "metadata": results["metadatas"][0][i],
                        "similarity_score": 1 - results["distances"][0][i],  # Convert distance to similarity
                        "id": results["ids"][0][i] if "ids" in results else None
                    })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching ChromaDB: {e}")
            return []
    
    def delete_document(self, document_hash: str) -> bool:
        try:
            # Get all chunks for this document
            results = self.collection.get(
                where={"document_hash": document_hash}
            )
            
            if results["ids"]:
                self.collection.delete(ids=results["ids"])
                logger.info(f"Deleted document {document_hash} from ChromaDB")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error deleting document from ChromaDB: {e}")
            return False

class RAGService:
    """Main RAG service for retrieval-augmented generation"""
    
    def __init__(self, vector_store_type: str = "chroma"):
        self.document_processor = DocumentProcessor()
        
        # Initialize vector store
        if vector_store_type == "chroma":
            self.vector_store = ChromaVectorStore()
        else:
            raise ValueError(f"Unsupported vector store type: {vector_store_type}")
        
        self.llm_service = llm_service
    
    def ingest_document(self, file_path: str) -> Dict[str, Any]:
        """Ingest a document into the RAG system"""
        try:
            # Process the document
            processed_doc = self.document_processor.process_file(file_path)
            
            # Add to vector store
            success = self.vector_store.add_documents(
                processed_doc["chunks"],
                processed_doc["metadata"]
            )
            
            if success:
                return {
                    "success": True,
                    "message": f"Successfully ingested {processed_doc['chunk_count']} chunks",
                    "document_hash": processed_doc["metadata"]["document_hash"],
                    "chunk_count": processed_doc["chunk_count"],
                    "metadata": processed_doc["metadata"]
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to add document to vector store"
                }
                
        except Exception as e:
            logger.error(f"Error ingesting document: {e}")
            return {
                "success": False,
                "message": f"Error ingesting document: {str(e)}"
            }
    
    def query(self, question: str, top_k: int = None, provider: str = None, **kwargs) -> Dict[str, Any]:
        """Perform RAG query - retrieve relevant chunks and generate answer"""
        top_k = top_k or Config.TOP_K_RESULTS
        
        try:
            # Retrieve relevant chunks
            relevant_chunks = self.vector_store.search(question, top_k=top_k)
            
            if not relevant_chunks:
                return {
                    "success": False,
                    "message": "No relevant documents found for the query"
                }
            
            # Filter by similarity threshold
            filtered_chunks = [
                chunk for chunk in relevant_chunks 
                if chunk["similarity_score"] >= Config.SIMILARITY_THRESHOLD
            ]
            
            if not filtered_chunks:
                return {
                    "success": False,
                    "message": f"No documents found above similarity threshold of {Config.SIMILARITY_THRESHOLD}"
                }
            
            # Prepare context for LLM
            context = self._prepare_context(filtered_chunks)
            
            # Generate system message
            system_message = """You are an AI assistant that answers questions based on the provided context. 
Use only the information from the context to answer questions. If the context doesn't contain 
enough information to answer the question, say so clearly."""
            
            # Create prompt
            prompt = f"""Context:
{context}

Question: {question}

Please provide a comprehensive answer based on the context provided above."""
            
            # Generate response using LLM
            llm_response = self.llm_service.generate_response(
                prompt=prompt,
                provider_name=provider,
                system_message=system_message,
                **kwargs
            )
            
            return {
                "success": True,
                "question": question,
                "answer": llm_response["response"] if llm_response["success"] else "Error generating response",
                "sources": [
                    {
                        "text": chunk["text"][:200] + "..." if len(chunk["text"]) > 200 else chunk["text"],
                        "file_name": chunk["metadata"]["file_name"],
                        "similarity_score": chunk["similarity_score"],
                        "chunk_index": chunk["metadata"]["chunk_index"]
                    }
                    for chunk in filtered_chunks
                ],
                "llm_provider": llm_response.get("provider"),
                "llm_model": llm_response.get("model"),
                "chunks_used": len(filtered_chunks)
            }
            
        except Exception as e:
            logger.error(f"Error performing RAG query: {e}")
            return {
                "success": False,
                "message": f"Error performing query: {str(e)}"
            }
    
    def _prepare_context(self, chunks: List[Dict[str, Any]]) -> str:
        """Prepare context string from retrieved chunks"""
        context_parts = []
        
        for i, chunk in enumerate(chunks, 1):
            file_name = chunk["metadata"]["file_name"]
            text = chunk["text"]
            score = chunk["similarity_score"]
            
            context_part = f"[Source {i} - {file_name} (Relevance: {score:.2f})]:\n{text}\n"
            context_parts.append(context_part)
        
        return "\n---\n".join(context_parts)
    
    def delete_document(self, document_hash: str) -> Dict[str, Any]:
        """Delete a document from the RAG system"""
        try:
            success = self.vector_store.delete_document(document_hash)
            
            if success:
                return {
                    "success": True,
                    "message": f"Successfully deleted document {document_hash}"
                }
            else:
                return {
                    "success": False,
                    "message": f"Document {document_hash} not found"
                }
                
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            return {
                "success": False,
                "message": f"Error deleting document: {str(e)}"
            }

# Initialize the global RAG service
try:
    if CHROMADB_AVAILABLE and SENTENCE_TRANSFORMERS_AVAILABLE:
        rag_service = RAGService()
        RAG_SERVICE_AVAILABLE = True
    else:
        rag_service = None
        RAG_SERVICE_AVAILABLE = False
        print("Warning: RAG service not available - missing dependencies")
except Exception as e:
    rag_service = None
    RAG_SERVICE_AVAILABLE = False
    print(f"Warning: Could not initialize RAG service: {e}")
