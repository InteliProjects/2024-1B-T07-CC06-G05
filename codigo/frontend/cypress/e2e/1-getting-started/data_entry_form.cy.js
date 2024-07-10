describe('Formulário de Configuração de Leitura', () => {
    it('deve preencher e submeter o formulário com valores válidos', () => {
      cy.visit('http://localhost:5173'); // URL da página do formulário
      
      // Comando para selecionar e fazer upload do arquivo
      cy.get('input[type="file"]').selectFile('cypress/fixtures/dados.csv');
  
      // Outros comandos para preencher o formulário
      cy.get('input[name="days"]').type('22');
      cy.get('input[name="hoursDay"]').type('6');
      cy.get('input[name="leituristas"]').type('5');
      cy.get('input[name="readTime"]').type('3');
  
      cy.get('select[name="algorithm"]').select('1');
      cy.get('button[type="submit"]').click();
  
      // Verificações após a submissão
      cy.url().should('include', '/resultados');
    //   cy.contains('Texto que você espera encontrar na página').should('be.visible');
    });
  });
  