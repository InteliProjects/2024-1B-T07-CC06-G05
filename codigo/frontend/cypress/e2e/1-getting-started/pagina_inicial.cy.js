describe('Teste da Página Inicial', () => {
    it('deve carregar a página inicial corretamente', () => {
      cy.visit('http://localhost:5173/');  // Certifique-se de que a URL está correta
      cy.url().should('include', 'localhost:5173'); // Verifica se a URL inclui 'localhost:5173'
    });
});
