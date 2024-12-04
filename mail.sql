CREATE TABLE mailinfo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customername TEXT NOT NULL,
    address TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    CHECK (
        LENGTH(customername) <= 255 AND 
        TRIM(customername) <> '' AND
        customername NOT LIKE '.%' AND
        customername NOT LIKE '%.' AND
        INSTR(customername, '  ') = 0 -- 禁止連續空格
    ),
    CHECK (
        LENGTH(address) <= 255 AND 
        TRIM(address) <> '' AND
        address NOT LIKE '.%' AND
        address NOT LIKE '%.' AND
        INSTR(address, '  ') = 0 -- 禁止連續空格
    ),
    CHECK (
        LENGTH(email) <= 255 AND 
        email LIKE '%@%' AND
        email LIKE '%.%' AND
        email NOT LIKE '..%' AND
        email NOT LIKE '.%@%' AND
        email NOT LIKE '%@.%' -- 禁止連續特殊字符或非法模式
    )
);
