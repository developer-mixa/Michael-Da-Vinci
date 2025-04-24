-- migrate:up

CREATE TABLE IF NOT EXISTS likes (
    id SERIAL PRIMARY KEY,
    target_user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    sender_user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_like_combination UNIQUE (sender_user_id, target_user_id)
);

CREATE INDEX IF NOT EXISTS idx_likes_target_user ON likes(target_user_id);

CREATE INDEX IF NOT EXISTS idx_likes_sender_user ON likes(sender_user_id);

-- migrate:down