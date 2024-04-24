-- Criação da tabela para o exemplo
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    idade INTEGER,
    cidade VARCHAR(100)
);


-- Inserção de dados de exemplo
INSERT INTO usuarios (nome, email, idade, cidade)
VALUES 
    ('Maria Oliveira', 'maria@example.com', 25, 'Rio de Janeiro'),
    ('Pedro Santos', 'pedro@example.com', 35, 'Salvador'),
    ('Ana Costa', 'ana@example.com', 28, 'Belo Horizonte');
