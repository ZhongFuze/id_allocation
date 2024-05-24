CREATE TABLE id_allocation (
    id SERIAL PRIMARY KEY,
    unique_id VARCHAR(265) NOT NULL,
    graph_id VARCHAR(255) NOT NULL,
    platform VARCHAR(255) NOT NULL,
    identity VARCHAR(255) NOT NULL,
    updated_nanosecond BIGINT DEFAULT 0,
    picked_time TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_index UNIQUE (unique_id)
);

CREATE INDEX idx_platform ON id_allocation (platform);
CREATE INDEX idx_graph_id_updated_time ON id_allocation (graph_id, updated_nanosecond);


CREATE OR REPLACE FUNCTION process_id_allocation(
    vids text[],
    new_graph_id varchar(255),
    new_updated_nanosecond bigint
)
RETURNS TABLE(return_graph_id varchar(255), return_updated_nanosecond bigint) AS $$
DECLARE
    existing_record RECORD;
    min_updated_record RECORD;
BEGIN
    -- Find the record with the minimum updated_nanosecond
    SELECT graph_id, updated_nanosecond INTO min_updated_record
    FROM id_allocation
    WHERE unique_id = ANY(vids)
    ORDER BY updated_nanosecond
    LIMIT 1;

    IF min_updated_record IS NOT NULL THEN
        -- Return the graph_id and updated_nanosecond with the smallest updated_nanosecond
        return_graph_id := min_updated_record.graph_id;
        return_updated_nanosecond := min_updated_record.updated_nanosecond;

        -- Update the table with the smallest updated_nanosecond
        UPDATE id_allocation
        SET graph_id = return_graph_id, updated_nanosecond = return_updated_nanosecond, picked_time = CURRENT_TIMESTAMP
        WHERE unique_id = ANY(vids);

        -- Insert new records that do not exist in the table
        FOR existing_record IN
            SELECT unnest(vids) AS unique_id
        LOOP
            INSERT INTO id_allocation (unique_id, graph_id, platform, identity, updated_nanosecond, picked_time)
            VALUES (
                existing_record.unique_id,
                new_graph_id,
                split_part(existing_record.unique_id, ',', 1),
                split_part(existing_record.unique_id, ',', 2),
                new_updated_nanosecond,
                CURRENT_TIMESTAMP
            )
            ON CONFLICT (unique_id) DO NOTHING; -- Ensure no duplicates
        END LOOP;

    ELSE
        -- Insert all records since no existing records were found
        FOR existing_record IN
            SELECT unnest(vids) AS unique_id
        LOOP
            INSERT INTO id_allocation (unique_id, graph_id, platform, identity, updated_nanosecond, picked_time)
            VALUES (
                existing_record.unique_id,
                new_graph_id,
                split_part(existing_record.unique_id, ',', 1),
                split_part(existing_record.unique_id, ',', 2),
                new_updated_nanosecond,
                CURRENT_TIMESTAMP
            );
        END LOOP;

        -- Return the input graph_id and updated_nanosecond since no existing records were found
        return_graph_id := new_graph_id;
        return_updated_nanosecond := new_updated_nanosecond;
    END IF;

    RETURN QUERY SELECT return_graph_id, return_updated_nanosecond;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM process_id_allocation(
    ARRAY['twitter,chan_izaki65652', 'farcaster,gytred', 'ethereum,0x61ae970ac67ff4164ebf2fd6f38f630df522e5ef'],
    'aec0c81c-7ab2-42e6-bb74-e7ea8d2cf903',
    1716471514174958
);