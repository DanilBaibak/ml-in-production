DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'interactions') THEN
        CREATE TYPE interactions AS ENUM ('bought', 'returned', 'replaced');
    END IF;
END
$$;

CREATE TABLE IF NOT EXISTS interaction (
    id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    amount INT NOT NULL,
    interaction_type interactions,
    interaction_date DATE NOT NULL
);
