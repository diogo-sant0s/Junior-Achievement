-- Cria a tabela license_keys
CREATE TABLE IF NOT EXISTS license_keys (
    id SERIAL PRIMARY KEY,
    key_code VARCHAR(255) NOT NULL UNIQUE,
    is_used BOOLEAN DEFAULT FALSE,
    used_by VARCHAR(255)
);

-- Insere algumas chaves de teste
INSERT INTO license_keys (key_code) VALUES
    ('2D074C46857B11947'),
    ('TESTE-123-ABC'),
    ('CHAVE-ATIVAR-001'),
    ('ABCDEF123456'),
    ('PLANO-GRATIS-2025');
