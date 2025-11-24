import unittest
import sys
import os
from unittest.mock import patch, mock_open

# Adiciona o diretório src ao path para importar os módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from geratxt import geraTxt

class TestGeraTxt(unittest.TestCase):
    
    @patch('builtins.input', side_effect=[1, 22, 1, '101-103'])
    @patch('builtins.open', new_callable=mock_open)
    def test_gera_txt_sucesso(self, mock_file, mock_input):
        """Testa a geração do arquivo de configuração com sucesso"""
        # Executa a função
        ramal, display, all_password, contexto, pick_group = geraTxt()
        
        # Verifica se a função retornou os valores esperados
        self.assertIsInstance(ramal, list)
        self.assertIsInstance(display, list)
        self.assertIsInstance(all_password, list)
        self.assertEqual(contexto, 22)
        self.assertEqual(pick_group, 1)
        
        # Verifica se o arquivo foi aberto para escrita
        mock_file.assert_called_once()
        
        # Verifica se as listas têm o tamanho esperado
        # Para 1 andar com faixa 101-103, esperamos 3 apartamentos * 4 letras = 12 ramais
        self.assertEqual(len(ramal), 12)
        self.assertEqual(len(display), 12)
        self.assertEqual(len(all_password), 12)
        
        # Verifica se os ramais foram gerados corretamente
        self.assertIn('2210101', ramal)  # Primeiro ramal (contexto + andar + 0 + unidade)
        self.assertIn('2210304', ramal)  # Último ramal
        
        # Verifica se as senhas têm o comprimento correto (9 caracteres)
        for senha in all_password:
            self.assertEqual(len(senha), 9)
            
        # Verifica se os displays foram gerados corretamente
        self.assertIn('Apto 101 A', display)
        self.assertIn('Apto 103 D', display)
    
    @patch('builtins.input', side_effect=['a', 'b'])  # Entradas inválidas
    def test_gera_txt_entrada_invalida(self, mock_input):
        """Testa o tratamento de entradas inválidas"""
        try:
            geraTxt()
            self.fail("Deveria ter lançado ValueError para entrada inválida")
        except ValueError:
            # Esperado que lance ValueError para entrada inválida
            pass
    
    @patch('builtins.input', side_effect=[1, 22, 1, '101-103'])
    @patch('builtins.open', side_effect=PermissionError)
    def test_gera_txt_erro_arquivo(self, mock_open, mock_input):
        """Testa o tratamento de erro ao escrever no arquivo"""
        with self.assertRaises(PermissionError):
            geraTxt()

if __name__ == '__main__':
    unittest.main()
