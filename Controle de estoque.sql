Create Database controle_estoque;
Use controle_estoque;

Create table usuario (
	usuario_id int auto_increment primary key,
    usuario varchar(50) unique not null,
    senha_hash varchar(255) not null,
    perfil enum('admin', 'usuario') default 'usuario'
);

Create table produtos (
	produto_id int auto_increment primary key,
    nome varchar(100) not null,
    categoria varchar(50),
    estoque_minimo int not null
);

Create table estoque (
	estoque_id int auto_increment primary key,
    produto_id int not null,
    quantidade int not null,
    foreign key (produto_id) references produtos(produto_id)
);

CREATE TABLE movimentacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    produto_id INT,
    tipo VARCHAR(20),
    quantidade INT,
    data_movimentacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (produto_id) REFERENCES produtos(produto_id)
);


Insert into usuario (usuario, senha_hash, perfil) values 
('admin', SHA2('admin123', 256), 'admin');

Insert into produtos (nome, categoria, estoque_minimo) values
('Arroz 5kg', 'Alimentos', 20),
('Feijão 1kg', 'Alimentos', 15),
('Detergente', 'Limpeza', 10); 

Insert into estoque (produto_id, quantidade) values
(1, 8),
(2, 18),
(3, 3);

Select
	p.nome as produto,
    p.categoria,
    e.quantidade as em_estoque,
    p.estoque_minimo,
    (p.estoque_minimo - e.quantidade) as falta
From produtos p 
join estoque e on p.produto_id = e.produto_id
where e.quantidade < p.estoque_minimo
order by falta desc; 



