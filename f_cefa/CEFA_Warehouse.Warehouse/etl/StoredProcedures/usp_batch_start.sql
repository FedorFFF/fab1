CREATE   PROCEDURE etl.usp_batch_start
    @process_name    VARCHAR(500),
    @stage_name      VARCHAR(500), 
    @sf_user_id      VARCHAR(500),
    @pipeline_run_id VARCHAR(500),
    @new_batch_id    BIGINT OUTPUT  -- Добавили выходной параметр
AS
BEGIN
    -- 1. Вычисляем новый ID и записываем его в переменную @new_batch_id
    SELECT @new_batch_id = ISNULL(MAX(sf_batch_id), 0) + 1 FROM etl.batches;

    -- 2. Вставляем запись, используя нашу переменную
    INSERT INTO etl.batches (
        sf_batch_id,
        process_name, 
        stage_name, 
        batch_status, 
        is_success,
        dtm_start, 
        sf_user_id, 
        pipeline_run_id
    )
    VALUES (
        @new_batch_id,
        @process_name, 
        @stage_name, 
        0, 
        0, 
        CAST(SYSDATETIME() AS DATETIME2(0)), 
        @sf_user_id, 
        @pipeline_run_id
    );

    -- 3. Возвращаем через SELECT для Fabric Pipeline
    SELECT @new_batch_id AS new_batch_id;
END;