USE db_enterprise;

CREATE TABLE t_company_addr (
  `id`    INT NOT NULL PRIMARY KEY AUTO_INCREMENT
  COMMENT 'id',
  `cname` VARCHAR(128) COMMENT '公司名称',
  `addr`  VARCHAR(128) COMMENT '地址',
  UNIQUE KEY `idx_cname`(cname)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8
  COMMENT '公司地址表'