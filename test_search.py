#!/usr/bin/env python3
"""
Test script for search functionality
"""
from app import app, db
from models import Pessoa
import re

def test_search(busca):
    print(f"\n=== TESTANDO BUSCA: '{busca}' ===")
    
    with app.app_context():
        # Simular a lógica de busca do route
        busca_cpf = re.sub(r'[^0-9]', '', busca)
        
        pessoas = Pessoa.query.filter(
            db.or_(
                # Busca por CPF (removendo formatação)
                Pessoa.cpf.like(f'%{busca}%'),
                # Busca por CPF sem formatação
                db.func.replace(db.func.replace(db.func.replace(Pessoa.cpf, '.', ''), '-', ''), '/', '').like(f'%{busca_cpf}%'),
                # Busca por nome (case insensitive)
                Pessoa.nome.ilike(f'%{busca}%')
            )
        ).order_by(Pessoa.nome).all()
        
        print(f"Resultados encontrados: {len(pessoas)}")
        for pessoa in pessoas:
            print(f"  {pessoa.cpf} - {pessoa.nome}")

if __name__ == "__main__":
    # Testes
    test_search("Eduardo")  # Busca por nome
    test_search("345")      # Busca por parte do CPF
    test_search("345.033.968-03")  # Busca por CPF completo
    test_search("ALEX")     # Busca por nome em maiúscula
    test_search("213736408")  # Busca por CPF sem formatação