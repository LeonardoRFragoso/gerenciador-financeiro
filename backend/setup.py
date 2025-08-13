#!/usr/bin/env python
"""
Script de inicialização do backend Django
Execute este script para configurar o banco de dados e criar dados iniciais
"""

import os
import sys
import subprocess

def run_command(command):
    """Executa um comando e retorna o resultado"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar: {command}")
        print(f"   {e.stderr}")
        return False

def run_migrations():
    """Executa as migrações do banco de dados"""
    print("🔄 Executando migrações...")
    if run_command("python manage.py makemigrations"):
        run_command("python manage.py migrate")
        print("✅ Migrações concluídas!")
    else:
        print("❌ Erro nas migrações")

def main():
    """Função principal"""
    print("🚀 Configurando Backend Django - Finance Control")
    print("=" * 50)
    
    setup_django()
    run_migrations()
    create_superuser()
    create_demo_user()
    
    print("\n✅ Setup concluído com sucesso!")
    print("\n📋 Próximos passos:")
    print("1. Execute: python manage.py runserver")
    print("2. Acesse: http://localhost:8000/api/docs/ (Documentação)")
    print("3. Admin: http://localhost:8000/admin/")
    print("4. Teste a API com o usuário demo (demo/demo123)")

if __name__ == '__main__':
    main()
