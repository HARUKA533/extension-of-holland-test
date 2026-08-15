import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    page_title="霍兰德职业兴趣测评（进阶专业版）",
    page_icon="🎯",
    layout="centered"
)

# ================= 题库与维度定义 (每部分 10 题，共 60 题) =================
sections_data = [
    {
        "key": "R", "title": "第一部分", "name": "现实型 (R)",
        "tagline": "动手 / 机械 / 物理实体 / 技术操作",
        "questions": [
            "喜欢组装、拆卸或修理机械、电子设备、家具等实物。",
            "喜欢动手类活动（如做木工、做模型、烹饪烘焙、园艺种植）。",
            "偏好去户外、现场、车间或实验室走动，而不是整天坐在办公室。",
            "对各种物理工具、精密仪器、软件控制界面上手极快。",
            "喜欢具体、看得到摸得着的成果，胜过抽象的概念讨论。",
            "动手能力强，遇到物品故障第一反应是拆开探究并尝试修好。",
            "喜欢学习一门扎实的硬核技术、设备操控或工程工艺。",
            "乐于参与体力、运动或需要空间协调、身体敏捷度的活动。",
            "相较于人际博弈，更喜欢和机器、程序、材料或自然环境打交道。",
            "享受从无到有亲手把一个物理产品/原型打磨制作出来的过程。"
        ],
        "traits": "务实落地、行动力极强、讲求实效、擅长物理空间与实体系统的构建与调校。",
        "advantage": "在 AI 与数字化深入发展的时代，软硬件协同调试、现场工程控制、精密制造与物理世界落地能力具有天然的高壁垒与不可替代性。",
        "modern_jobs": [
            "智能硬件 / 机器人调试与运维专家",
            "新能源汽车三电系统 / 智能座舱测试工程师",
            "3D 打印与精密制造工艺架构师",
            "无人机飞控系统 / 物联网传感器技术专家",
            "智能仓储自动化 / 现场工程系统架构师"
        ]
    },
    {
        "key": "I", "title": "第二部分", "name": "研究型 (I)",
        "tagline": "逻辑 / 思考 / 探究 / 钻研",
        "questions": [
            "喜欢刨根问底，遇到不懂的机制、算法或原理一定要彻底搞清楚。",
            "喜欢阅读硬核科普、深度行业研报、学术论文或技术解析文章。",
            "遇到复杂问题时，本能地倾向于用逻辑推理、实验数据和证据寻找答案。",
            "享受独立思考和逻辑推演的过程，不畏惧抽象的数学、逻辑与代码构架。",
            "喜欢做深度研究、数据建模、市场底层归因或实验论证。",
            "对“事物背后的底层因果规律”的兴趣远大于“别人都在怎么做”。",
            "擅长在海量杂乱的信息中抽丝剥茧，总结出结构化的核心规律。",
            "习惯用批判性思维审视现有观点，不盲从权威与常识。",
            "对探索未知领域、攻克技术/学术难关有长久的内在驱动力。",
            "做决定时更依赖客观事实和数据支撑，而非主观情感或从众心理。"
        ],
        "traits": "理智敏锐、逻辑严密、以好奇心驱动、深度思考者，擅长抽象建模与底层归因。",
        "advantage": "在信息爆炸时代，能穿透表象直达本质，在算法研发、复杂系统决策、技术突破与深度研判上处于核心价值链顶端。",
        "modern_jobs": [
            "AI 算法研究员 / 提示词架构师 (Prompt Engineer)",
            "大数据科学家 / 商业智能 (BI) 决策建模专家",
            "量化金融策略师 / 宏观行业深度分析师",
            "生物信息学 / 基因计算与医药研发科学家",
            "复杂软件系统架构师 / 深度科技智库顾问"
        ]
    },
    {
        "key": "A", "title": "第三部分", "name": "艺术型 (A)",
        "tagline": "创意 / 审美 / 自由 / 表达",
        "questions": [
            "喜欢非结构化、高自主度的环境，抗拒僵化死板的条条框框与打卡制度。",
            "喜欢通过视觉设计、写作、音乐、摄影、剪辑或代码美学来表达自我。",
            "对美感、色彩搭配、版式构图、文字韵味或空间质感极其敏锐。",
            "经常有打破常规的奇思妙想，喜欢尝试前所未有的创新玩法。",
            "情绪感知力极强，容易被优秀的内容作品、电影或音乐深深触动。",
            "宁可承担一定的不确定性，也不愿意每天重复按部就班的流水线工作。",
            "喜欢研究前沿潮流、青年文化、视觉艺术或人机交互的情感体验。",
            "做事情讲究“调性”与“独特性”，讨厌千篇一律的同质化输出。",
            "擅长运用隐喻、直觉和故事思维来打动受众或阐述观点。",
            "在充满自由与启发的工作氛围中，能迸发出极强的工作爆发力。"
        ],
        "traits": "审美出众、直觉敏锐、反传统、情绪丰沛，善于创造独特的情感共鸣与非标内容。",
        "advantage": "在同质化与标准化泛滥的时代，审美溢价、情绪共鸣构建与非线性创新是品牌打造、爆款策划与破圈传播的稀缺驱动力。",
        "modern_jobs": [
            "UI/UX 交互体验总监 / 情感化人机交互设计师",
            "AIGC 视觉创作者 / AI 生成艺术指导",
            "游戏世界观架构师 / 剧情与关卡体验设计师",
            "新媒体独立内容主理人 / 创意品牌视觉顾问",
            "沉浸式空间与数字多媒体艺术策展人"
        ]
    },
    {
        "key": "S", "title": "第四部分", "name": "社会型 (S)",
        "tagline": "助人 / 倾听 / 赋能 / 人际",
        "questions": [
            "擅长倾听他人心声，朋友遇到困惑或情绪低落时经常主动向你倾诉。",
            "乐于帮助他人解决成长难题，教会别人掌握新技能会让你非常有成就感。",
            "喜欢人际互动与跨部门团队协作，胜过长时间完全封闭独处工作。",
            "能迅速捕捉到别人微妙的情绪变化，并给出温暖、得体的回应。",
            "对心理学、教育培训、个人成长、公益或高价值社群运营充满兴趣。",
            "认为工作的终极意义在于“切实改善他人的生活质量或带来长期社会价值”。",
            "在团队中擅长扮演润滑剂与调解者角色，化解冲突并凝聚人心。",
            "更愿意相信人性的善意，乐于发掘并激发他人的潜能与闪光点。",
            "擅长一对一深度交流，能建立深层次的信任感与安全感。",
            "对如何设计更具人文关怀的产品、服务或体验流程有深刻体会。"
        ],
        "traits": "高同理心、利他导向、善于沟通赋能、注重心理连接与人际生态的健康度。",
        "advantage": "技术越冰冷，情绪价值与人文温度就越昂贵。深度共情、信任构建、高敏沟通与社群凝聚力是最难被算法自动化取代的核心能力。",
        "modern_jobs": [
            "专业心理咨询师 / 个人职业生涯发展教练",
            "核心客户成功专家 (CSM) / 高净值私域社群主理人",
            "组织文化发展 (OD) / 员工成长与体验架构师",
            "现代知识博主导师 / 在线学习体验设计师",
            "大健康管理咨询师 / 身心康复辅导顾问"
        ]
    },
    {
        "key": "E", "title": "第五部分", "name": "企业型 (E)",
        "tagline": "领导 / 说服 / 商业变现 / 目标驱动",
        "questions": [
            "喜欢牵头项目、组织活动，乐于在团队中担任拍板定夺的核心主导者。",
            "喜欢向别人推销自己的观点、项目或产品，并有信心说服对方买单。",
            "目标感极强，享受竞争、追逐高目标，渴望更高的社会地位与财富回报。",
            "敢于冒险并承受压力，在资源有限或局势不明朗时敢于果断决策。",
            "乐于主动结交各领域有影响力的人脉，善于建立互利共赢的合作网络。",
            "嗅觉敏锐，经常在日常生活中琢磨如何把事情做大、变现或规模化运营。",
            "擅长调动、整合各方资源（人、钱、渠道）去达成既定的战略目标。",
            "在公开演讲、路演或关键商务谈判场合能展现出强大的气场与感染力。",
            "面对挫折和阻力有极强的心理韧性，能迅速复盘并调整打法重新进攻。",
            "喜欢掌舵全局、驱动业务增长，胜过只负责局部技术细节。"
        ],
        "traits": "极强目标驱动、野心与魄力兼备、精于说服与资源整合、商业敏锐度极高。",
        "advantage": "擅长在不确定性中穿透迷雾，将技术、创意与人才高效打包并推向市场实现商业闭环，是商业机构不可或缺的领航者与开拓者。",
        "modern_jobs": [
            "商业化出海业务合伙人 / 独立出海商业主理人",
            "AI / 科技产品商业化总监 (GTM Lead)",
            "战略级大客户解决方案总监 (B2B Solution VP)",
            "早期硬科技投资经理 / 风险投资机构投后顾问",
            "品牌联名与跨界商业拓展 (BD) 操盘手"
        ]
    },
    {
        "key": "C", "title": "第六部分", "name": "常规型 (C)",
        "tagline": "秩序 / 细节 / 流程标准化 / 风控合规",
        "questions": [
            "喜欢井井有条的环境，电脑文件、桌面、行程安排必须分类归档清晰。",
            "擅长数据比对、文本校验、逻辑纠错，对细微瑕疵有极高的敏感度。",
            "喜欢明确的规则、标准作业流程（SOP），胜过模棱两可、边界不清的任务。",
            "承诺的事情必定按时、保质、严谨交付，具有极强的计划性与执行纪律。",
            "擅长梳理繁杂的账目、法律合同、数据资产、档案或合规性资料。",
            "看到混乱无序的业务流程或因为粗心导致的低级失误会非常难以容忍。",
            "善于将一次性的成功经验拆解、沉淀为可复制、标准化的工作指引。",
            "重视风险防范与数据安全，能提前发现流程漏洞并设置防护机制。",
            "在处理大量结构化数据或重复性核验时，能保持长时间的高准确率与耐心。",
            "更倾向于稳健、确定性高的推进节奏，讨厌朝令夕改和不可控的风险。"
        ],
        "traits": "严谨精细、高度自律、恪守规则、精于流程梳理与风险控制，追求零差错交付。",
        "advantage": "当业务从 0 到 1 走向 1 到 100 时，能够构建坚实运转的底层系统与制度屏障，是组织规模化扩张与持续安全运行的底盘基石。",
        "modern_jobs": [
            "企业数据合规与算法伦理风控官",
            "财务自动化 (RPA) 与商业流程审计专家",
            "敏捷项目流程经理 (Scrum Master) / QA 质量体系专家",
            "跨境电商供应链履约与精细化运营总监",
            "数字化资产与企业知识库架构师"
        ]
    }
]

# 30 种两两复合跨界细化方案
cross_field_map = {
    "RI": "软硬件协同开发、物联网 (IoT) 架构、精密科学仪器研发、工业机器人底层控制系统",
    "RA": "工业产品外观造型设计、建筑结构与空间艺术、电影级实体特效道具与机电动效开发",
    "RS": "高级实操技能导师、运动机能与物理康复专家、户外极限运动安全与现场培训",
    "RE": "智能硬件硬件创业主理人、新能源工程项目操盘手、硬科技解决方案售前总监",
    "RC": "自动化测试流水线架构师、供应链质量品控 (QA) 总监、精密设备运维标准化管理",
    "IR": "自动驾驶感知算法研发、生物医药湿实验计算分析、智能仿生机械结构研发",
    "IA": "游戏核心玩法与数值架构师、交互数据可视化专家、深度科技类智库撰稿人",
    "IS": "用户体验深度研究员 (UX Researcher)、循证心理学与认知科学家、跨学科教育产品研发",
    "IE": "硬科技早期风险投资人 (VC)、前沿科技商业化产品战略专家、SaaS 商业化架构师",
    "IC": "量化金融风控建模师、数据安全合规分析师、高价值知识产权与专利检索专家",
    "AR": "新媒体沉浸式互动装置艺术家、高级定制珠宝/工艺设计师、科技舞台视效总监",
    "AI": "生成式 AI (AIGC) 艺术总监、沉浸式剧情体验与世界观设计师、计算美学研究员",
    "AS": "艺术疗愈师、品牌共鸣与情绪价值策划、创作者社区生态构建者",
    "AE": "创意广告操盘总监、潮流消费品牌独立主理人、数字文化 IP 孵化与授权经理",
    "AC": "企业级 Design System 规范架构师、高精度排版与数字资产管理主管、UI 质检总监",
    "SR": "职业康复训练师、实操技能公益赋能导师、体验式团队拓展总教练",
    "SI": "组织人才发展架构师 (TD)、认知行为辅导专家、教育测量与认知诊断顾问",
    "SA": "表达性艺术心理咨询师、非营利组织品牌共鸣主理人、青年创意成长营导师",
    "SE": "组织变革与企业文化合伙人、高价值社群商业化总裁、私域客户生态运营总监",
    "SC": "教务与学术标准运营总监、人力资源信息系统 (HRIS) 专家、员工关怀合规主管",
    "ER": "技术型工业制造出海主理人、重大工程商务谈判总监、新能源设备全球供应链拓展",
    "EI": "战略咨询合伙人、硬科技商业孵化器总监、企业数字化转型首席顾问",
    "EA": "全域整合营销与品牌传播总监、影视/游戏制作人、网红经济机构 (MCN) 合伙人",
    "ES": "企业高管教练 (Executive Coach)、大客户关系管理副总裁、跨国多元文化协作推动者",
    "EC": "企业首席运营官 (COO)、供应链金融风险控制总监、企业并购重组商务合规总监",
    "CR": "工业工程 (IE) 流程效率优化专员、数据中心物理基础设施运维主管、实验室质量体系内审员",
    "CI": "数据治理与合规架构师、金融量化风控审计师、网络安全情报分析师",
    "CA": "交互设计规范工程师、数字出版与排版标准主管、多媒体素材质量控制专家",
    "CS": "高管事务与运营流程管理总监、企业内部标准合规培训师、客户体验质量控制体系主管",
    "CE": "企业 ERP 实施战略顾问、商业运营合规总监、财务数字化与税务筹划总监"
}

# ================= 状态管理 =================
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.scores = {}

st.title("🎯 霍兰德职业兴趣倾向测评")
st.caption("基于国际 RIASEC 模型 · 60 题深度测评 · 全面解析与空间投影")

# ================= 测试作答流 =================
if st.session_state.step < len(sections_data):
    current = sections_data[st.session_state.step]
    
    st.info("💡 **测试规则**：凭第一直觉判断，不要考虑薪资、地位或“能力行不行”，只看“喜不喜欢/乐不乐意做”。")
    
    # 仅展示“第X部分”，不展示具体类型
    st.markdown(f"### {current['title']}")
    
    # 进度条
    st.progress(st.session_state.step / len(sections_data))

    with st.form(key=f"form_{current['key']}"):
        answers = []
        for idx, q in enumerate(current["questions"]):
            ans = st.radio(
                f"{idx+1}. {q}",
                options=["是", "否"],
                index=None,
                horizontal=True,
                key=f"{current['key']}_q_{idx}"
            )
            answers.append(ans)
        
        btn_label = "提交并查看完整深度报告" if st.session_state.step == len(sections_data) - 1 else "下一部分"
        submitted = st.form_submit_button(btn_label)
        
        if submitted:
            if any(a is None for a in answers):
                st.error("⚠️ 本部分还有题目未选择，请全部选择后再提交。")
            else:
                score = sum(1 for a in answers if a == "是")
                st.session_state.scores[f"{current['key']}-实际得分"] = score
                st.session_state.step += 1
                st.rerun()

# ================= 结果报告页面 =================
else:
    # 提取六维度分数 (0~10 分)
    scores = {s["key"]: st.session_state.scores.get(f"{s['key']}-实际得分", 0) for s in sections_data}
    total_score = sum(scores.values())
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    # 前三位代码
    top3_code = "".join([item[0] for item in sorted_scores[:3]])
    top1_key, top2_key, top3_key = sorted_scores[0][0], sorted_scores[1][0], sorted_scores[2][0]
    
    sec_dict = {s["key"]: s for s in sections_data}
    first_type, second_type, third_type = sec_dict[top1_key], sec_dict[top2_key], sec_dict[top3_key]

    # ---------- 计算心理测量学指标 ----------
    # 1. 分化度 (Differentiation Index) = 最高分 - 最低分 (范围 0~10)
    diff_index = sorted_scores[0][1] - sorted_scores[-1][1]
    if diff_index >= 6:
        diff_status = "高度分化（极度清晰）"
        diff_desc = "你的职业偏好边界极其清晰，优势区与排斥区对比鲜明，职业选择决策效率极高。"
    elif diff_index >= 3:
        diff_status = "中度分化（健康平衡）"
        diff_desc = "你的兴趣倾向重点突出，同时具备良好的综合适应力，可塑性强。"
    else:
        diff_status = "低分化（多潜能/扁平）"
        diff_desc = "各维度得分相对接近，表明你具备多向探索潜能，或处于职业定位重塑期。"

    # 2. 六角形一致性 (Consistency Index)
    # 六边形顺序：R - I - A - S - E - C
    hex_order = ['R', 'I', 'A', 'S', 'E', 'C']
    idx1 = hex_order.index(top1_key)
    idx2 = hex_order.index(top2_key)
    distance = min(abs(idx1 - idx2), 6 - abs(idx1 - idx2))
    
    if distance == 1:
        consistency_status = "高一致性（天然协同）"
        consistency_desc = f"{top1_key} 与 {top2_key} 在六角形上完全相邻，内在动机高度自洽，职业发展顺畅，极少产生内在角色冲突。"
    elif distance == 2:
        consistency_status = "中一致性（互补多能）"
        consistency_desc = f"{top1_key} 与 {top2_key} 处于中度关联区域，兼具深度与拓展性，非常适合做复合型业务中枢。"
    else: # distance == 3 (对角线)
        consistency_status = "对角张力（跨界破局）"
        consistency_desc = f"{top1_key} 与 {top2_key} 位于对角线两端（如动手 vs 人际、严谨 vs 自由）。这种组合常伴随心理内在张力，但也是诞生跨界颠覆型人才的温床。"

    # 3. Prediger 二维空间世界地图投影
    # Things vs People: TP = 2.00*R + 1.00*I - 1.00*A - 2.00*S - 1.00*E + 1.00*C
    # Data vs Ideas: DI = 0.00*R - 1.73*I - 1.73*A + 0.00*S + 1.73*E + 1.73*C
    r, i_sc, a, s, e, c = scores['R'], scores['I'], scores['A'], scores['S'], scores['E'], scores['C']
    tp_score = 2.0 * r + 1.0 * i_sc - 1.0 * a - 2.0 * s - 1.0 * e + 1.0 * c
    di_score = - 1.73 * i_sc - 1.73 * a + 1.73 * e + 1.73 * c

    # 页面标题
    st.success(f"## 🏆 您的霍兰德职业代码：**{top3_code}**")
    st.caption(f"主导模式：{first_type['name'].split()[0]}（主） + {second_type['name'].split()[0]}（辅） + {third_type['name'].split()[0]}（辅）")

    # 四大标签页
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 六角雷达与能量占比", 
        "🧭 心理模型与空间投影", 
        "🧠 主导特质深度解析", 
        "💼 现代职业与跨界建议"
    ])

    # ================= 标签页 1：图表展示 =================
    with tab1:
        st.markdown("#### 1. 六维多边形雷达图 (0–10分)")
        categories = ['现实型(R)', '研究型(I)', '艺术型(A)', '社会型(S)', '企业型(E)', '常规型(C)']
        keys_order = ['R', 'I', 'A', 'S', 'E', 'C']
        values = [scores[k] for k in keys_order]
        
        categories_closed = categories + [categories[0]]
        values_closed = values + [values[0]]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values_closed,
            theta=categories_closed,
            fill='toself',
            fillcolor='rgba(79, 70, 229, 0.25)',
            line=dict(color='#4f46e5', width=2),
            name='得分'
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            showlegend=False,
            height=340,
            margin=dict(l=40, r=40, t=20, b=20)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        st.markdown("#### 2. 特质能量分布与占比")
        if total_score > 0:
            pie_labels = [s["name"] for s in sections_data]
            pie_values = [scores[s["key"]] for s in sections_data]
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=pie_labels,
                values=pie_values,
                hole=.45,
                marker=dict(colors=['#3b82f6', '#8b5cf6', '#ec4899', '#10b981', '#f59e0b', '#64748b'])
            )])
            fig_pie.update_layout(height=260, margin=dict(l=20, r=20, t=10, b=10))
            st.plotly_chart(fig_pie, use_container_width=True)

            # 进度条
            for s in sections_data:
                sc = scores[s['key']]
                pct = (sc / total_score) * 100
                st.write(f"**{s['name']}**：`{sc} / 10 分`（占比 **{pct:.1f}%**）")
                st.progress(pct / 100)
        else:
            st.warning("所有项目得分为 0，无法计算能量占比。")

    # ================= 标签页 2：进阶指标 =================
    with tab2:
        st.markdown("### 🔬 心理测量学进阶模型诊断")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("剖面分化度 (Differentiation)", f"{diff_index} 分", diff_status)
        with col_b:
            st.metric("六角一致性 (Consistency)", f"距离: {distance}", consistency_status)

        st.markdown(f"• **分化度解读**：{diff_desc}")
        st.markdown(f"• **一致性解读**：{consistency_desc}")

        st.markdown("---")
        st.markdown("#### 🗺️ Prediger 职场世界地图坐标投影")
        st.caption("根据心理学空间模型将六维度加权投射至「事物-人际 (Things-People)」与「数据-理念 (Data-Ideas)」两极轴：")

        # 绘制二维散点图
        fig_scatter = go.Figure()
        
        # 绘制象限背景区域
        fig_scatter.add_vline(x=0, line_dash="dash", line_color="#cbd5e1")
        fig_scatter.add_hline(y=0, line_dash="dash", line_color="#cbd5e1")

        # 标注用户点
        fig_scatter.add_trace(go.Scatter(
            x=[tp_score],
            y=[di_score],
            mode='markers+text',
            marker=dict(size=14, color='#4f46e5'),
            text=["📍 你的核心落点"],
            textposition="top center"
        ))

        fig_scatter.update_layout(
            xaxis=dict(title="← 偏好【人际/社群】 (People) | (Things) 偏好【事务/物理】 →", range=[-25, 25]),
            yaxis=dict(title="← 偏好【抽象/理念】 (Ideas) | (Data) 偏好【数据/规则】 →", range=[-25, 25]),
            height=360,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    # ================= 标签页 3：深度特质解析 =================
    with tab3:
        st.markdown(f"### 核心主导特质：{first_type['name']}")
        st.write(f"**核心标签：** `{first_type['tagline']}`")
        
        st.markdown("**🧠 你的特质表现：**")
        st.write(first_type["traits"])
        
        st.markdown("**⚡ 现代社会/职场核心竞争力：**")
        st.write(first_type["advantage"])

        st.markdown("---")
        st.markdown("#### 辅助动力源：")
        st.markdown(f"- **次级主导特质（{second_type['name']}）：** {second_type['traits']}")
        st.markdown(f"- **协同潜能特质（{third_type['name']}）：** {third_type['traits']}")

    # ================= 标签页 4：现代职业与细化跨界 =================
    with tab4:
        st.markdown(f"### 🎯 优先探索的现代职业领域（基于 {first_type['name'].split()[0]}）")
        for job in first_type["modern_jobs"]:
            st.markdown(f"- **{job}**")

        st.markdown("---")
        
        # 获取复合代码（例如 IA 或 AI）
        cross_pair_key = f"{top1_key}{top2_key}"
        cross_desc = cross_field_map.get(cross_pair_key, "跨领域综合实践与创新管理专家")
        
        st.markdown(f"### 🔀 深度复合跨界方向：**{cross_pair_key} 组合**")
        st.caption(f"当 **{first_type['name'].split()[0]}** 遇到 **{second_type['name'].split()[0]}**")
        
        st.info(f"💡 **前沿跨界赛道与岗位推荐：**\n\n{cross_desc}")
        
        st.markdown("#### 🚀 职业发展策略建议：")
        st.write(f"1. **以 {first_type['name'].split()[0]} 为基石**：将主导维度的能力打磨成最硬核的个人护城河。")
        st.write(f"2. **以 {second_type['name'].split()[0]} 为杠杆**：运用次级特质进行差异化跨界竞争，形成独特的个人 IP。")
        st.write(f"3. **警惕内耗**：当一致性偏向张力组合时，学会在不同项目阶段切换工作心智，避免在细节与全局中反复纠结。")

    st.markdown("---")
    if st.button("🔄 重新进行测评"):
        st.session_state.step = 0
        st.session_state.scores = {}
        st.rerun()
