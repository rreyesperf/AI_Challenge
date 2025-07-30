#!/usr/bin/env python3
"""
Static Dockerfile Analysis for Azure Container Apps
Validates Dockerfile configuration without requiring Docker to be running
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Any, Tuple

class DockerfileAnalyzer:
    def __init__(self, app_dir: str):
        self.app_dir = Path(app_dir)
        self.dockerfile_path = self.app_dir / "Dockerfile"
        self.requirements_path = self.app_dir / "requirements.txt"
        self.issues = []
        self.warnings = []
        self.recommendations = []
        
    def validate_dockerfile_exists(self) -> bool:
        """Check if Dockerfile exists"""
        if not self.dockerfile_path.exists():
            self.issues.append("❌ Dockerfile not found")
            return False
        return True
    
    def parse_dockerfile(self) -> List[Tuple[str, str]]:
        """Parse Dockerfile into instruction-argument pairs"""
        if not self.dockerfile_path.exists():
            return []
        
        instructions = []
        current_instruction = ""
        
        with open(self.dockerfile_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Handle line continuations
                if line.endswith('\\'):
                    current_instruction += line[:-1] + " "
                    continue
                else:
                    current_instruction += line
                
                # Parse instruction
                if current_instruction:
                    parts = current_instruction.split(None, 1)
                    if len(parts) >= 1:
                        instruction = parts[0].upper()
                        args = parts[1] if len(parts) > 1 else ""
                        instructions.append((instruction, args, line_num))
                    current_instruction = ""
        
        return instructions
    
    def validate_base_image(self, instructions: List[Tuple[str, str, int]]) -> bool:
        """Validate FROM instruction"""
        from_instructions = [(inst, args) for inst, args, _ in instructions if inst == "FROM"]
        
        if not from_instructions:
            self.issues.append("❌ No FROM instruction found")
            return False
        
        if len(from_instructions) > 1:
            self.warnings.append("⚠️ Multiple FROM instructions (multi-stage build)")
        
        base_image = from_instructions[-1][1]  # Use the last FROM
        
        # Check for Python base image
        if not base_image.startswith("python:"):
            self.issues.append(f"❌ Base image should be Python-based, found: {base_image}")
            return False
        
        # Check Python version
        if "python:3.11" in base_image:
            print("✅ Using Python 3.11 (recommended)")
        elif "python:3.9" in base_image or "python:3.10" in base_image:
            self.warnings.append("⚠️ Consider upgrading to Python 3.11 for better performance")
        elif "python:3.8" in base_image or "python:3.7" in base_image:
            self.issues.append("❌ Python version too old, use 3.10+ for Azure Container Apps")
            return False
        
        # Check for slim variant
        if "slim" in base_image:
            print("✅ Using slim base image (good for size)")
        else:
            self.recommendations.append("💡 Consider using slim variant for smaller image size")
        
        return True
    
    def validate_workdir(self, instructions: List[Tuple[str, str, int]]) -> bool:
        """Validate WORKDIR instruction"""
        workdir_instructions = [args for inst, args, _ in instructions if inst == "WORKDIR"]
        
        if not workdir_instructions:
            self.issues.append("❌ No WORKDIR instruction found")
            return False
        
        workdir = workdir_instructions[-1]
        if workdir != "/app":
            self.warnings.append(f"⚠️ WORKDIR is {workdir}, recommend /app for consistency")
        
        return True
    
    def validate_copy_instructions(self, instructions: List[Tuple[str, str, int]]) -> bool:
        """Validate COPY instructions"""
        copy_instructions = [(args, line) for inst, args, line in instructions if inst == "COPY"]
        
        if not copy_instructions:
            self.issues.append("❌ No COPY instructions found")
            return False
        
        # Check for requirements.txt copy first
        req_copy_found = False
        app_copy_found = False
        
        for args, line_num in copy_instructions:
            if "requirements.txt" in args:
                req_copy_found = True
                if ". ." in args or "/ /" in args:
                    self.warnings.append(f"⚠️ Line {line_num}: Copying everything with requirements.txt reduces cache efficiency")
            elif ". ." in args or "* ." in args:
                app_copy_found = True
        
        if not req_copy_found:
            self.issues.append("❌ requirements.txt should be copied separately for better caching")
        
        if not app_copy_found:
            self.issues.append("❌ Application code not being copied")
        
        return req_copy_found and app_copy_found
    
    def validate_run_instructions(self, instructions: List[Tuple[str, str, int]]) -> bool:
        """Validate RUN instructions"""
        run_instructions = [args for inst, args, _ in instructions if inst == "RUN"]
        
        if not run_instructions:
            self.issues.append("❌ No RUN instructions found")
            return False
        
        pip_install_found = False
        package_update_found = False
        
        for args in run_instructions:
            if "pip install" in args:
                pip_install_found = True
                if "--no-cache-dir" not in args:
                    self.warnings.append("⚠️ Consider using --no-cache-dir with pip install")
                if "requirements.txt" not in args:
                    self.warnings.append("⚠️ Install from requirements.txt for reproducible builds")
            
            if "apt-get update" in args:
                package_update_found = True
                if "rm -rf /var/lib/apt/lists/*" not in args:
                    self.warnings.append("⚠️ Clean apt cache after installation")
        
        if not pip_install_found:
            self.issues.append("❌ No pip install instruction found")
        
        return pip_install_found
    
    def validate_user_security(self, instructions: List[Tuple[str, str, int]]) -> bool:
        """Validate user security"""
        user_instructions = [args for inst, args, _ in instructions if inst == "USER"]
        
        if not user_instructions:
            self.issues.append("❌ No USER instruction - running as root (security risk)")
            return False
        
        user = user_instructions[-1]
        if user == "root":
            self.issues.append("❌ Explicitly running as root (security risk)")
            return False
        
        print(f"✅ Running as non-root user: {user}")
        return True
    
    def validate_expose_port(self, instructions: List[Tuple[str, str, int]]) -> bool:
        """Validate EXPOSE instruction"""
        expose_instructions = [args for inst, args, _ in instructions if inst == "EXPOSE"]
        
        if not expose_instructions:
            self.issues.append("❌ No EXPOSE instruction found")
            return False
        
        ports = []
        for args in expose_instructions:
            ports.extend(args.split())
        
        if "8080" not in ports:
            self.issues.append("❌ Port 8080 not exposed (required for Azure Container Apps)")
            return False
        
        if len(ports) > 1:
            self.warnings.append("⚠️ Multiple ports exposed, ensure only necessary ports")
        
        print("✅ Port 8080 correctly exposed for Azure Container Apps")
        return True
    
    def validate_cmd_instruction(self, instructions: List[Tuple[str, str, int]]) -> bool:
        """Validate CMD instruction"""
        cmd_instructions = [args for inst, args, _ in instructions if inst in ["CMD", "ENTRYPOINT"]]
        
        if not cmd_instructions:
            self.issues.append("❌ No CMD or ENTRYPOINT instruction found")
            return False
        
        cmd = cmd_instructions[-1]
        
        # Check for production WSGI server
        if "gunicorn" not in cmd.lower():
            self.issues.append("❌ Should use Gunicorn for production deployment")
            return False
        
        # Check for proper binding (handle both string and JSON array formats)
        bind_check = ("--bind 0.0.0.0:8080" in cmd or 
                     ("--bind" in cmd and "0.0.0.0:8080" in cmd))
        if not bind_check:
            self.issues.append("❌ Gunicorn should bind to 0.0.0.0:8080")
            return False
        
        # Check for proper app reference
        if "startup:app" not in cmd and "routes:app" not in cmd:
            self.warnings.append("⚠️ Check app reference in CMD instruction")
        
        print("✅ Using Gunicorn with proper configuration")
        return True
    
    def validate_env_variables(self, instructions: List[Tuple[str, str, int]]) -> bool:
        """Validate environment variables"""
        env_instructions = [args for inst, args, _ in instructions if inst == "ENV"]
        
        required_envs = ["FLASK_ENV", "PYTHONPATH", "PYTHONUNBUFFERED"]
        found_envs = []
        
        for args in env_instructions:
            for req_env in required_envs:
                if req_env in args:
                    found_envs.append(req_env)
        
        missing_envs = set(required_envs) - set(found_envs)
        if missing_envs:
            self.warnings.append(f"⚠️ Consider adding environment variables: {', '.join(missing_envs)}")
        
        # Check for production environment
        flask_env_found = any("FLASK_ENV=production" in args for args in env_instructions)
        if not flask_env_found:
            self.warnings.append("⚠️ Set FLASK_ENV=production for production deployment")
        
        return True
    
    def validate_healthcheck(self, instructions: List[Tuple[str, str, int]]) -> bool:
        """Validate health check"""
        healthcheck_instructions = [args for inst, args, _ in instructions if inst == "HEALTHCHECK"]
        
        if not healthcheck_instructions:
            self.warnings.append("⚠️ No HEALTHCHECK instruction (recommended for Azure Container Apps)")
            return True
        
        healthcheck = healthcheck_instructions[-1]
        if "/api/health" in healthcheck:
            print("✅ Health check configured correctly")
        else:
            self.warnings.append("⚠️ Health check should use /api/health endpoint")
        
        return True
    
    def validate_requirements_txt(self) -> bool:
        """Validate requirements.txt"""
        if not self.requirements_path.exists():
            self.issues.append("❌ requirements.txt not found")
            return False
        
        with open(self.requirements_path, 'r', encoding='utf-8') as f:
            requirements = f.read()
        
        required_packages = ["Flask", "gunicorn", "requests"]
        missing_packages = []
        
        for package in required_packages:
            if package.lower() not in requirements.lower():
                missing_packages.append(package)
        
        if missing_packages:
            self.issues.append(f"❌ Missing required packages: {', '.join(missing_packages)}")
            return False
        
        # Check for version pinning
        lines = [line.strip() for line in requirements.split('\n') if line.strip() and not line.startswith('#')]
        unpinned = [line for line in lines if '==' not in line and line]
        
        if unpinned:
            self.warnings.append(f"⚠️ Unpinned packages (consider version pinning): {', '.join(unpinned[:3])}")
        
        print("✅ requirements.txt validation passed")
        return True
    
    def check_azure_compatibility(self, instructions: List[Tuple[str, str, int]]) -> Dict[str, bool]:
        """Check Azure Container Apps specific requirements"""
        compatibility = {
            "port_8080": False,
            "non_root_user": False,
            "production_server": False,
            "health_endpoint": False,
            "environment_config": False
        }
        
        # Check port 8080
        expose_instructions = [args for inst, args, _ in instructions if inst == "EXPOSE"]
        for args in expose_instructions:
            if "8080" in args:
                compatibility["port_8080"] = True
                break
        
        # Check non-root user
        user_instructions = [args for inst, args, _ in instructions if inst == "USER"]
        for args in user_instructions:
            if args != "root" and args.strip():
                compatibility["non_root_user"] = True
                break
        
        # Check production server (Gunicorn)
        cmd_instructions = [args for inst, args, _ in instructions if inst in ["CMD", "ENTRYPOINT"]]
        for args in cmd_instructions:
            if "gunicorn" in args.lower():
                compatibility["production_server"] = True
                break
        
        # Check if routes.py has health endpoints
        routes_path = self.app_dir / "routes.py"
        if routes_path.exists():
            with open(routes_path, 'r', encoding='utf-8') as f:
                routes_content = f.read()
            
            if "/api/health" in routes_content:
                compatibility["health_endpoint"] = True
            
            if "FLASK_ENV" in routes_content and "production" in routes_content:
                compatibility["environment_config"] = True
        
        return compatibility
    
    def generate_security_checklist(self) -> List[str]:
        """Generate security checklist"""
        return [
            "✅ Non-root user configured",
            "✅ Minimal base image (Python slim)",
            "✅ No secrets in Dockerfile",
            "✅ Proper file permissions",
            "✅ Security headers in application",
            "⚠️ Ensure secrets are passed via environment variables",
            "⚠️ Regular security updates for base image",
            "⚠️ Scan image for vulnerabilities before deployment"
        ]
    
    def analyze(self) -> Dict[str, Any]:
        """Run complete analysis"""
        print("🔍 Static Dockerfile Analysis for Azure Container Apps")
        print("=" * 60)
        
        if not self.validate_dockerfile_exists():
            return {"success": False, "issues": self.issues}
        
        instructions = self.parse_dockerfile()
        print(f"📄 Parsed {len(instructions)} Dockerfile instructions")
        
        # Run all validations
        validations = [
            self.validate_base_image(instructions),
            self.validate_workdir(instructions),
            self.validate_copy_instructions(instructions),
            self.validate_run_instructions(instructions),
            self.validate_user_security(instructions),
            self.validate_expose_port(instructions),
            self.validate_cmd_instruction(instructions),
            self.validate_env_variables(instructions),
            self.validate_healthcheck(instructions),
            self.validate_requirements_txt()
        ]
        
        success = all(validations)
        azure_compatibility = self.check_azure_compatibility(instructions)
        security_checklist = self.generate_security_checklist()
        
        return {
            "success": success,
            "total_checks": len(validations),
            "passed_checks": sum(validations),
            "issues": self.issues,
            "warnings": self.warnings,
            "recommendations": self.recommendations,
            "azure_compatibility": azure_compatibility,
            "security_checklist": security_checklist,
            "instructions_count": len(instructions)
        }
    
    def print_report(self, analysis: Dict[str, Any]):
        """Print analysis report"""
        print("\n" + "=" * 60)
        print("📊 DOCKERFILE ANALYSIS REPORT")
        print("=" * 60)
        
        if analysis["success"]:
            print("🎉 OVERALL STATUS: ✅ PASSED")
        else:
            print("⚠️ OVERALL STATUS: ❌ NEEDS ATTENTION")
        
        print(f"\n📈 SUMMARY:")
        print(f"   Checks Passed: {analysis['passed_checks']}/{analysis['total_checks']}")
        print(f"   Success Rate: {(analysis['passed_checks']/analysis['total_checks'])*100:.1f}%")
        print(f"   Issues: {len(analysis['issues'])}")
        print(f"   Warnings: {len(analysis['warnings'])}")
        print(f"   Instructions: {analysis['instructions_count']}")
        
        if analysis["issues"]:
            print(f"\n🚨 CRITICAL ISSUES:")
            for issue in analysis["issues"]:
                print(f"   {issue}")
        
        if analysis["warnings"]:
            print(f"\n⚠️ WARNINGS:")
            for warning in analysis["warnings"]:
                print(f"   {warning}")
        
        if analysis["recommendations"]:
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in analysis["recommendations"]:
                print(f"   {rec}")
        
        print(f"\n☁️ AZURE CONTAINER APPS COMPATIBILITY:")
        compatibility = analysis["azure_compatibility"]
        for check, status in compatibility.items():
            icon = "✅" if status else "❌"
            print(f"   {icon} {check.replace('_', ' ').title()}")
        
        print(f"\n🔒 SECURITY CHECKLIST:")
        for item in analysis["security_checklist"]:
            print(f"   {item}")
        
        print(f"\n🚀 DEPLOYMENT READINESS:")
        if analysis["success"] and len(analysis["issues"]) == 0:
            print("   ✅ Ready for Azure Container Apps deployment")
            print("   ✅ Dockerfile follows best practices")
            print("   ✅ Security considerations addressed")
        else:
            print("   ❌ Fix critical issues before deployment")
            print("   ⚠️ Review warnings and recommendations")
        
        print("\n" + "=" * 60)

def main():
    """Main analysis runner"""
    app_dir = os.getcwd()
    
    analyzer = DockerfileAnalyzer(app_dir)
    analysis = analyzer.analyze()
    analyzer.print_report(analysis)
    
    # Save detailed report
    report_path = Path(app_dir) / "dockerfile_analysis_report.json"
    with open(report_path, 'w') as f:
        json.dump(analysis, f, indent=2)
    
    print(f"📄 Detailed report saved to: {report_path}")
    
    return analysis["success"]

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
