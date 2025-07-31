主要规则：
    如果主表没有变动，则其他三张表也不会产生变动
    出现以下情况不上线照面主表、照面 ar 表、照面 ae 表、照面历史表：
        通过 getSourceIsOnline() 检查地方公示源是否允许上线到主表dwd，如果不允许则不上线
        如果新企业主表照面信息的核准日期为空，不上线
        如果新企业主表照面信息的核准日期比主库旧，不上线
        当企业照面上线标志位校验未通过，且该企业未配置 code_type=1（t_dwd_filter_value_config表中的字段 code_type  = 1）时，即如果贴源照面（local贴源照面主表）无变化，主表照面也不上线
        如果主表照面信息只有一个字段发生变更，且是 source_type 字段，不上线
        如果主表照面信息无字段变更，不上线


具体业务逻辑：
    

业务步骤 1：t_dwd_entinfo_ent_baseinfo（照面主表）新旧数据对比，生成t_dwd_entinfo_ent_baseinfo_ar（照面ar 表）、t_dwd_entinfo_ent_baseinfo_ae（照面ae 表）数据
        数据准备与初始化
            获取企业ID和新旧企业照面信息
            判断是新增（A）还是更新（U）操作
            设置字段标志fieldFlagDTO
        通过 getSourceIsOnline() 检查地方公示源是否允许上线到主表dwd，如果不允许则不上线照面主表、ar 、ae 表、历史表
        convertAllFields() 转换所有字段，通过调用各个字段的转换方法
        默认设置主表上线标志"merge"字段为 true，若后续对比新旧数据无差异则更改为 false
        核准日期校验规则：
            如果核准日期为空，不上线照面主表、ar、ae 表、历史表
            如果新数据的核准日期比主库旧，不上线 照面主表、ar、ae 表、历史表
            对 gjgs 源的特殊处理：如果新旧数据的核准日期相等 ，线上企业状态为注/吊销状态时，增量为在营状态时，如果增量为GS外他源时，不能更新entstatus 和 statusdisplay字段
        当企业照面上线标志位校验未通过，且该企业未配置 code_type=1（t_dwd_filter_value_config表中的字段 code_type  = 1）中时， return，不上线 ar、ae 表、历史表
        调用dwdTFieldsPriorityService.compareFieldPriority 进行字段优先级处理
        开始对比
            如果旧企业照面信息不为空（更新场景）：
                dealDate() : 处理日期字段，用旧值填充新数据中的空值
                convertIndustry() : 转换转换行业代码 industryco 和行业门类 industryphy
                如果是注销、吊销企业复活，需要清空注销日期等字段 新增码值一样情况下保持中文一致
                delEntStatus() : 处理企业状态变更（如注销企业复活时清空注销日期）
                delGtToEnt() : 处理个体工商户转企业的特殊逻辑
                compareFields()：对两个CompanyInfo对象的字段进行比较，并记录变更
                如果存在变更：
                    如果只有一个字段发生变更，且是 source_type 字段：
                        不上线照面主表、ar、ae 表、历史表
                    否则
                        调用 saveChangesToAr() 保存 AR 表变更记录，记录变更前的数据源类型
                        创建 AE 记录，设置 entid、singal_id、ds_code、ops为"U"、idt 为旧数据 idt、before 为旧企业照面信息、after 为新企业照面信息
                如果无字段变更：不上线照面主表、ar、ae 表、历史表
            如果旧企业照面信息为空（新增场景）：
                调用EntBaseInfoUtil.convertIndustry 设置行业代码industryco 和行业门类industryphy
                创建 AE 记录，设置 entid、singal_id、ds_code，after 字段为新企业照面信息、ops为"A"、idt 为当前时间戳
                如果当前企业的企业类型（enttype）属于("4531","4532","4533","5400","5410","5420","5430","6400","6410","6420","6430")，则将 PipelineContext 中的 updateLegalent 标志位设置为 true
    

业务步骤2：更新t_dwd_entinfo_ent_baseinfo（照面主表），更新主表历史拉链t_dwd_entinfo_ent_baseinfo_history（照面历史表）
        初始化和分支机构预处理
            对分支机构类型（企业类型属于BRANCH_OFFICE）的企业进行特殊处理，清空注册资金相关字段（regcap、regcapcur、regcapcurdisplay）
        模块化数据合并处理，通过缓存标识控制各模块是否执行
            判断当前企业处理上下文中是否已包含“alert”标记，若未包含则执行历史变更信息的合并处理mergeAlterRecords()
            判断当前企业处理上下文中是否已包含“abnormal”标记，若未包含则执行经营异常的合并处理mergeAbnormal()
            判断当前企业处理上下文中是否已包含“apprdateFlag”标记，若未包含则执行股东信息初始化partnersMerge()和高管信息初始化employMerge()
        如果当前企业处理上下文中"merge"字段为 false：照面主表不上线
        如果企业照面上线标志位校验未通过，且该企业未配置 code_type=1（t_dwd_filter_value_config，code_type = 1）时，照面主表不上线
        照面主表上线：将前面合并处理后的企业照面信息保存到数据库
        更新主表历史拉链：
            结束上一个历史版本的有效期（endTime设置为当前时间）
            新建一条历史记录（startTime=现在，endTime=null）