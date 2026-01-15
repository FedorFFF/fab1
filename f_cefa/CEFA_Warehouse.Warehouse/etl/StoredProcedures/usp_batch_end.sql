CREATE   PROCEDURE etl.usp_batch_end
    @sf_batch_id  BIGINT,
    @is_success   SMALLINT, -- Теперь SMALLINT (1: Success, 0: Error, 2: Warning и т.д.)
    @cnt_ins      BIGINT = NULL,
    @cnt_upd      BIGINT = NULL,
    @cnt_del      BIGINT = NULL
AS
BEGIN
    -- В Fabric UPDATE всегда требует точного соответствия типов
    UPDATE etl.batches
    SET batch_status = CASE 
                            WHEN @is_success = 1 THEN 1  -- Успех
                            WHEN @is_success = 0 THEN -1 -- Ошибка
                            ELSE 2                       -- Другое (например, Warning)
                       END,
        is_success   = @is_success,
        dtm_end      = CAST(SYSDATETIME() AS DATETIME2(0)),
        cnt_ins_rows = ISNULL(@cnt_ins, cnt_ins_rows),
        cnt_upd_rows = ISNULL(@cnt_upd, cnt_upd_rows),
        cnt_del_rows = ISNULL(@cnt_del, cnt_del_rows)
    WHERE sf_batch_id = @sf_batch_id;
END;