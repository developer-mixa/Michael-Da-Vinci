-- migrate:up

CREATE TYPE user_status AS ENUM (
    'ACTIVE',
    'NO_ACTIVE'
);

CREATE TYPE gender AS ENUM (
    'GIRL',
    'MAN'
);

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(128) NOT NULL,
    description VARCHAR(1024) NOT NULL,
    date_of_birth DATE NOT NULL,
    telegram_id BIGINT UNIQUE NOT NULL,
    status user_status NOT NULL,
    gender gender NOT NULL
);

CREATE UNIQUE INDEX uq_user_telegram_id ON users (telegram_id);

-- migrate:down