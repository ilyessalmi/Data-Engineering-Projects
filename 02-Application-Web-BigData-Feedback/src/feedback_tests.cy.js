
describe('Feedback Tests', () => {
  beforeEach(() => {
    // Visitez la page d'accueil avant chaque test
    cy.visit('http://localhost:5000');
  });

  it('should submit a feedback', () => {
            /// Les étapes du test seront écrites ic /// 
    // Remplissez le formulaire de feedback
    cy.get('select[name="formation"]').select('Data Engineering');
    cy.get('select[name="typeRetour"]').select('Contenu du cours');
    cy.get('input[name="date"]').type('2023-05-29');
    cy.get('input[name="rating"]').type('5');
    cy.get('textarea[name="comments"]').type('cours interessant.');
    cy.get('input[name="consentement"]').check();

    // Soumettez le formulaire
    cy.get('form').submit();

    // Vérifiez que la soumission a réussi
    cy.contains('Merci pour votre contribution ! votre retour a été enregistré.').should('be.visible');
  });

  /*
  it('should display the list of feedbacks', () => {
    // Cliquez sur le lien pour afficher la liste des feedbacks
    cy.contains('Voir tous les retours').click();

    // Vérifiez que la liste des feedbacks est affichée
    cy.wait(10000)
    cy.contains('Liste des retours').should('be.visible');
    cy.url().should('include', '/feedbacks');
  });
  */

});