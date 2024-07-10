import unittest
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        # Cria uma instância do Flask para testes
        self.app = app.test_client()
        # Define o ambiente de testes
        self.app.testing = True

    def test_send_data(self):
        # Prepara a requisição com um arquivo de teste
        test_file = open("test_data.txt", "rb")
        data = {"data": (test_file, "test_data.txt")}
        
        # Envia a requisição para a rota /sendData
        response = self.app.post('/sendData', data=data, content_type='multipart/form-data')
        
        # Verifica se a resposta foi bem sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verifica se a resposta contém dados
        self.assertIsNotNone(response.data)
        
        # Verifica se a resposta está no formato JSON
        self.assertEqual(response.content_type, 'application/json')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()