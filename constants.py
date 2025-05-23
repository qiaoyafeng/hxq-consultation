# ########################################### 问诊参数 #######################################

CONSULT_STATUS_INIT = 1
CONSULT_STATUS_PROCESSING = 2
CONSULT_STATUS_DONE = 3
CONSULT_STATUS_REPORT = 4
CONSULT_STATUS_EVALUATION = 5

CONSULT_CASE_STATUS_NO = 0
CONSULT_CASE_STATUS_INIT = 1
CONSULT_CASE_STATUS_PROCESSING = 2
CONSULT_CASE_STATUS_DONE = 3
CONSULT_CASE_STATUS_ERROR = 4


# ########################################### LLM参数 #######################################

LLM_HXQ_PLAT_ID = 1  # hxq_llm
LLM_TONGYI_PLAT_ID = 2  # tongyi

LLM_HXQ_PLAT_DICT = {
    LLM_HXQ_PLAT_ID: "hxq_llm",
    LLM_TONGYI_PLAT_ID: "tongyi",
}

LLM_HXQ_MODEL_DS_R1_8B_ID = 1
LLM_HXQ_MODEL_DICT = {LLM_HXQ_MODEL_DS_R1_8B_ID: "deepseek-r1:8b"}

LLM_TONGYI_MODEL_QWEN_PLUS_ID = 1
LLM_TONGYI_MODEL_DICT = {LLM_TONGYI_MODEL_QWEN_PLUS_ID: "qwen-plus"}

# ########################################### 问题相关参数 #######################################

QUESTIONS = [
    "最近情绪怎么样？是正常，低落还是高涨？",
    "是整天低落，还是只有晚上低落？",
    "这种低落大概持续久？",
    "最近睡得好不好？",
    "睡眠怎么不好，是入睡困难，睡眠时间短，还是做梦多,还是睡眠浅",
    "大概需要多久入睡？",
    "醒来之后，过多久又能睡着？",
    "大概能睡几小时？",
    "睡起来感觉累吗？",
    "白天有没有感觉特别困，没精神？",
    "最近食欲怎么样？",
    "最近体重有明显下降吗？",
    "最近有没有觉得做事情没劲，不想动，什么都不想做？",
    "最近有没有做啥都感受不到快乐，即使是自己之前特别喜欢的事情也不快乐",
    "最近是不是感觉精力明显不足，做事总是觉得很累？",
    "最近有没有总是感觉比较疲惫？",
    "你有没有感到自己反应迟钝,经常不能及时反应别人的问题？",
    "现在有上班吗？",
    "有没有觉着自己工作效率下降了？例如做事比以前更费劲？更费时间了",
    "有在去学校上课吗？",
    "学习效率是否下降很多，相比于之前，明显需要花费更多的时间",
    "最近有没有总是在胡思乱想，感到特别烦躁？",
    "最近有没有注意力不集中，经常跟不上话题？",
    "最近总是特别自卑，觉着自己处处不如人",
    "最近做错事的时候，是不是总会特别自责，特别内疚？",
    "最近理解能力是不是下降很多，比起往常，需要花费更多时间理解",
    "最近记忆力怎么样",
    "最近有没有做一些伤害自己的行为？比例割腕，扎伤自己",
    "最近有没有觉着活着没有意思，想自杀的想法",
    "有自杀想法之后，有没有去做？",
    "实施自杀过程中，中途是否放弃了？",
    "在自杀过程中，是不是别被别人发现并制止？",
    "最近有没有感觉身体不适，例如有没有心慌、胸闷、出汗、尿频等？",
    "在你的经历中，有没有听到别人听不到的声音",
    "听到别人听不到的声音是之前有，还是现在有",
    "听到的声音是一个人的还是很多人的",
    "听到的声音有没有命令你去做一些事，尤其是伤害自己的事",
    "在后续有这种情况，你需要及时的寻求家人的帮助，帮你制止这种行为",
    "在你的经历中，有没有看到别人看不到的东西",
    "看到这些东西是以前有的，最近才有的，还是一直都有？",
    "看到别人看不到的东西，是经常发生还是偶尔有",
    "这种现象最近是更加频繁了，还是比之前少，还是和之前一样",
    "看到的人或物会不会命令你做一些事情，或者伤害你？",
    "有没有总是担心别人想伤害你，或者盯着你看",
    "有没有总是担心别人跟踪你，想偷你东西的想法",
    "最近有没有特别害怕陌生人，害怕到人多的场合，没有安全感",
    "最近有没有感到性欲减退，或者性生活感受不到快乐",
    "相对于正常时候，不能正常进行学习，或者社交变得困难",
    "你为此感到很痛苦，或者觉着活着没有意义",
    "相对于正常时候，无法进行工作，或者不能正常社交",
    "你为此感到很痛苦，或者觉着活着没有意义",
    "有没有感觉自己人际交往不能像其他正常人一样自然，自己的社交总是很困难",
    "相比于同龄人，学习能力差，或者不能学习，比起正常人差很多",
    "最近半年时间，您有没有正常去上班",
    "最近半年时间，您有没有觉着社交是一件困难的事情，发现自己不能正常去社交",
    "最近半年时间，您的生活可以自理吗？",
    "这种担心别人伤害你，或者盯着你看的想法，是否连续持续一个月以上",
    "这种担心偷你的东西或者跟踪你的想法，有没有连续持续一个月以上",
    "是否连续一个月以上都听到这种声音",
    "是否连续一个月以上都看到别人看不到的东西",
    "有没有出现讲话开始没逻辑？比如自言自语或者说一些别人不理解的疯言疯语",
    "这种言语紊乱现象，是否持续一个月以上？",
    "有没有出现过无理由的大喊大叫，或者摔东西的行为",
    "这种无理由的大喊大叫，或者摔东西的行为，是否持续发生一个月以上",
    "有没有出现过没有目的的，到处不停的走来走去",
    "这种不停的走来走去，是否持续一个月以上",
    "有没有做一些反复无目的的动作，如拨弄手指、反复拍摸或擦搓",
    "做这些重复动作，是否持续一个月以上",
    "有没有出现过活动极度降低，经常不说话，其他人询问也不回应",
    "这种迟钝或者发呆的行为，是否持续一个月以上",
    "有没有一直做一些怪异的面部表情，或者做怪异而有意的动作，如蹦跳或蹑行、对旁人敬礼等",
    "做这些怪异的行为，是否持续一个月以上",
    "最近，有没有感觉生活没意思，不想社交，也没什么活力",
    "这种消极生活的方式，是否持续一个月以上",
    "是否连续一个月以上,都是这种不快乐的状态",
    "以上回答为是的行为或者状态，是不是已经持续了半年以上？",
    "您是否对一些事情总是过度担心，例如担心不好的事情会发生在自己身上或者家人身上？",
    "当有这些担心的想法，您是否可以控制这些想法？",
    "最近有没有感到自己心情烦躁，坐不住？",
    "这种坐立不安，是经常有还是偶尔有",
    "有没有脑袋一片空白的感觉，突然什么都想不起来？",
    "最近是否特别容易生气，经常因为一件小事而发脾气",
    "最近是否经常感到全身紧张，肌肉紧绷",
    "生活和学习过程中，这种焦虑和担忧的状态，已经持续超过半年了吗？ ",
    "情绪高涨是比正常时候还要高兴还是和正常时候一样",
    "其他人有没有发现你比正常时候还要兴奋，变得异常兴奋",
    "最近有没有感觉自己比正常时候话变多了，说话速度也变快了，甚至可以很长时间讲话不停歇？",
    "最近有没有感觉到自己思维特别活跃，思路特别清晰，很多事都能很快想明白？",
    "有没有感觉到自己的思维有跳跃感，联想能力特别强，有一种飘忽的感觉？",
    "高兴时候有没有觉得自己最牛，干什么事都能成功",
    "最近是不是觉得自己状态特别好，特别棒，不能接受别人说自己不好？",
    "有没有想去做一些事，这些事是之前自己根本不敢想象的，或者之前根本不会去做的？",
    "最近是不是虽然睡得少，但是依然精力充沛，做事不停？",
    "有没有感觉自己精力充沛，并给自己制定了很多行动计划",
    "相比于正常的时候，个人活动明显变多了（外出活动，购物，旅游，学习等）",
    "在个人活动明显增多的情况下，不感觉到疲惫，依然精力旺盛",
    "有没有发现自己的注意力很难集中，总是随着想法或者事情变化而发生转移",
    "最近有没有突然花钱大手大脚，消费远远超出自己的能力范围，甚至有借钱，网贷等行为",
    "消费过后，对自己的冲动行为，感到非常后悔",
    "最近有没有社交活动突然增多，变得非常喜欢交朋友？",
    "最近有没有觉着自己性欲变得很强烈，性生活变多了？",
    "这种异常情绪高涨的情况，有没有连续持续一周以上的情况？",
    "您曾经有被诊断为躁狂吗？",
    "您曾经有被诊断为抑郁症吗？",
    "有没有对做过的事情，多次检查，反复确认？或者特别爱干净，需要反复洗手，洗澡？或者一直去想一件事情？",
    "这些强迫行为，您内心清楚是有必要去做，还是没必要去做？",
    "您是否可以控制自己不去做？",
    "您有没有对自己说过的话，或者门窗有没有关好，去反复确认？",
    "您有没有对没有意义的事情反复思考，比如：为什么太阳是圆的，不是方的？",
    "您有没有脑海中听到或看到某一观念或一句话，便自然而然地想到一些令人不快的事情，如，看到下雨就想到水灾；看到有人抽烟就想到大火等。",
    "您有没有看到一句话或脑中出现一个念头时，便不由自主地联想到相反的词句或观念。如想起“和平”，马上联想到“战争”；",
    "您有没有脑海中不由自主地反复出现经历过的事情",
    "您有没有有一种强烈的冲动想法，要去做某种违背自己意愿的事情，但实际上不会转变为行为如，站在高处，就有想要跳下去的冲动，虽然能控制自己不会真的跳下去，但却难以克制这个想法；",
    "您有没有怀疑自己是否忘记关门窗、电源、天然气等而反复检查",
    "您有没有反复洗手、洗澡或清洁屋子等行为，而且这种清洗往往要遵循一定的程序进行",
    "您有没有不能相信自己的所见所闻，为了消除这种怀疑所带来的焦虑，常反复询问他人给予解释或保证。如反复询问他人自己是否说错话，有无做错事等",
    "您有没有对数字产生了强迫观念，整日沉浸在无意义的计数动作中，如计数路人、偶然碰到的电话号码等，明知浪费了很多时间但无法控制自己",
    "您有没有一些强迫性仪式动作,如，进门一定要先迈左脚；鞋子要头朝东摆放；",
    "以上强迫思维或强迫行为，是否占用了你很多时间，您感觉到很痛苦，影响了正常生活？",
    "至少中间间隔2月以上，这中间是正常表现，以前出现过抑郁发作（症状和最近类似）吗？",
    "之前有没有被诊断为 躁狂发作，或者双向情感障碍",
    "有没有自残的想法",
    "有没有晚上睡的很多，白天醒不来的情况",
    "最近有没有查肝功，转氨酶有没有升高",
    "有没有头疼或者头晕的症状",
    "有没有便秘",
    "最近有没有做血清泌乳素测定，泌乳素水平怎么样",
    "有没有恶心，厌食,腹泻等肠胃问题",
    "身体上有没有起皮疹等过敏反应",
    "是否有手抖，嘴抖，眨眼睛，嘴麻，手头麻 等症状",
    "体重有增加很多吗",
    "月经规律吗",
]


IPT_QUESTIONS = [
    "最近怎么样？",
    "心情如何？",
    "有发生影响到情绪的事件吗？",
    "具体是什么时候发生的？",
    "虽然好像新的情况或最近的事情，让你很痛苦，但是其实是因为……（原本聚焦的问题）？",
    "我们的目标和之前是一致的，我们可以试着去聊聊现在的问题？",
    "在人际心理治疗里面，我们很强调人际关系。所以今天我们可以一起来汇总一下，你生活中这些重要的人际关系，帮我了解一下，你身边哪些人帮助和支持到你，哪些人又让你觉得有压力或影响到你的情绪。这里有一张纸，画了三个同心圆。我们把它叫做人际关系清单。你自己在最中心，我们用这个点表示。在这三个圆圈里，我要请你写上你目前生活中的人，最亲密的写在最内圈，关系一般的写在中间圈，比较远的写在外圈。可以是你的家人、朋友、亲戚、同事等等，一共写七到八个人，可以是名字或称呼。请你想一想，然后写下来。",
    "我看到你写了一些了。可以再想一想，是不是已经包括目前生活中所有重要的人了？",
    "好的。那接下来呢，我们会逐个讨论一下圈里的每个人。请你跟我讲讲你跟这个人的关系，ta是否有帮助或支持到你？以及你们的关系有没有令你不太满意的部分。你想先讲谁呢？",
    "那目前你跟他的关系怎么样呢？",
    "我要请你想一想，有没有什么时候你觉得这个人是理解你或者支持你的？",
    "现在我们要进行的是个案框架的讨论，你会发现，我这里面有涵盖4个大的因素，这四个部分分别是生物因素、心理因素、社会因素和文化因素，此次我们将一起去讨论看看有哪些因素其实是有在影响着我们的情绪。",
    "我们之前有讨论到生物因素，这次我们将后面的谈论完，然后确定我们的问题领域，先开始讨论心理因素，你会觉得是什么在影响着你的情绪状态？",
    "到现在我们的治疗已经进行到初期阶段的尾声部分，下一次我们即将进入到中期阶段，在开始前，我们可能要共同探讨后面我们的治疗目标是怎样的，制定两到三个小的治疗目标。",
    "你最近一次吵架或发生不愉快是什么时候？",
    "对于吵架或不愉快的诉求是什么？",
    "首先，我会需要跟你介绍下什么是角色扮演，以及具体包括哪几个部分，首先你要去描述最近一周内发生的一件比较严重的事情，然后我会扮演你的角色，你扮演有冲突对象的角色，例如妈妈，然后我们再去交换，你扮演你自己，我扮演冲突对象。然后在一起去探讨可以怎么去更改说话的方式？",
    "可以，那我们选择这个场景，现在我来扮演你，你扮演你的妈妈，这个时候你要代入进去，准备好了吗？",
    "是的，后面我也会和你的家属进行家长访谈，我们在治疗室说的内容我是会保密的，但是我也不是你们之间的传声筒，我会按照治疗的节奏进行。",
    "很好，所以角色扮演之后你现在会有怎样的感受？",
    "如果在图上挑一个最支持你的人，你认为是？理由是什么？",
    "如果挑一个和你冲突最激烈的人，你认为是？理由是什么？",
    "你们之间会发生什么样的冲突，你怎么理解？",
    "最近怎么样？这些冲突解决了吗？",
    "你在这份关系中有什么样的期待？",
    "现在如果需要你找一个时间和地点，这个时间地点是能够让你感觉很舒适的，很放松的一个环境，你会选择什么时候哪个地方？",
    "我们可以看到，一个问题，能滋生出很多问题，这些问题有时候看上去很不一样，但是其实根源仍然是在……我们要争取围绕这个问题，争取更多的支援和支持，当然，如果当前的问题真的完全解决了，或者不困扰你了，你也可以提出来，我们可以顺利结束咨询，或者我们可以聚焦在新的问题上，但是，我们始终要记得，IPT是一种目标明确的短程治疗",
    "自伤自伤的评估：曾经有过自伤的想法吗？",
    "曾经有过自伤的经历吗？",
    "具体是什么时候发生的？",
    "最近有发生吗？",
    "曾经有自杀的想法吗？",
    "曾经有自杀的实施吗？",
    "具体是什么时候？",
    "当时有发生什么事情吗？",
    "测评的分数大概上多少分？",
    "最近的一次影响到情绪的事件是什么时候？",
    "最严重的一次影响到情绪的事件是什么时候？",
    "最早的一次影响到情绪的事件是什么时候？",
]


# ########################################### LLM相关参数 #######################################
CONSULT_REPORT_PROMPT_TEMPLATE = """
【角色设定】
你是一位精神心理科的医生，擅长从对话中识别心理疾病特征。现在需要根据以下医患对话生成专业问诊报告：

【输入格式】
患者信息：{patient_info}
对话记录：{conversation}

【输出要求】
基本信息： 患者信息，包括姓名，性别，年龄
主述：文字不超过20字

现病史
起病时间：__年月日
主要症状及变化：__
伴随症状：____
诊疗经过（包括在其他医疗机构的治疗、用药情况等）：
既往史
既往疾病史：
手术外伤史：
过敏史：对____过敏（如有，请详细说明）
预防接种史：___
家族史
家族中有无类似疾病史：□ 有 □ 无（如有，请说明与患者的关系及疾病名称）
其他遗传性疾病或特殊病史：_____
体格检查
体温：℃ 脉搏：次/分 呼吸：次/分 血压：/____ mmHg
一般状况：□ 良好 □ 一般 □ 差
皮肤粘膜：
淋巴结：
头部五官：
颈部：____
胸部：心肺听诊：_
腹部：___
四肢及脊柱：
神经系统：____
辅助检查
1.__（检查名称及结果）
2.__（检查名称及结果）
3.其他（如有）：__
初步诊断
1.待排/鉴别诊断：__
治疗计划
1.药物治疗：_____
2.非药物治疗（如物理治疗、心理治疗等）：__
3.进一步检查建议：___
医嘱
1.饮食指导：_____
2.生活方式调整：_____
3.复诊时间：__年月__日
4.其他注意事项：_____
医生签名：_____
日期：__年月__日
此模板仅供参考，实际应用时请结合具体情况灵活调整，并确保所有信息的收集和处理符合医疗隐私保护法规的要求。

"""

# AI患者报告模版
CONSULT_PATIENT_REPORT_PROMPT_TEMPLATE = """
【角色设定】
你是一位精神心理科的医生，擅长从对话和患者提供的病历中识别心理疾病特征。现在需要根据以下医患对话和患者提供的病历生成问诊报告：

【输入格式】
对话记录：{conversation}
病历：{case_content}

【输出要求】
主诉：文字不超过20字
诊断：
治疗建议：

"""


# 报告评估模版
CONSULT_REPORT_EVALUATION_PROMPT_TEMPLATE = """
你是一名资深医疗质量评估专家，擅长从医患沟通记录、诊断报告和患者既往病历中分析医生的诊疗表现。请根据以下信息，对本次诊疗过程进行全面评估，并给出评分（百分制）和具体分析。

【患者基本信息及既往病历】：
病历：{case_content}

【医患聊天记录】：
对话记录：{conversation}

【医生填写的诊断报告】：
诊断报告:{report}

请你按照如下结构输出医生诊疗表现分析报告：

1. **总评分**：在100分制下给出评分
2. **分项评分分析**（可参考以下维度）：
   - 沟通与共情能力（是否倾听患者、是否安抚情绪等）
   - 临床判断准确性（是否基于病历和症状做出合理诊断）
   - 检查/检验建议的合理性
   - 用药建议/治疗方案的科学性
   - 诊断报告记录的规范性
3. **优点总结**
4. **需要改进的方面**
5. **总体评价与建议**

请确保你的分析语言客观、专业、具体，并有一定临床依据。

"""


CONSULT_HEALTH_ADVICE_PROMPT_TEMPLATE = """
【角色设定】
你是一位精神心理科的医生，擅长从对话中识别心理疾病特征。现在需要根据以下医患对话生成专业的健康建议。

【要求】
1. 只输出建议内容，不要包含任何标题、编号或其他说明文字；
2. 建议内容不得超过50字。

【输入格式】
医患对话：
{conversation}

【输出要求】
健康建议内容

【示例】
医患对话：
医生：最近感觉怎样？
患者：总是疲劳、失眠。

期望输出：
保持规律作息，适量运动，必要时就医调整。

"""


CONSULT_KEY_PHRASE_EXTRACTION_PROMPT_TEMPLATE = """
任务描述：
请对以下医患对话内容进行处理，完成以下任务：
1. 从文本中提取出关键的词汇（关键词）。
2. 对每个关键词计算词频（或权重，如 TF-IDF）。
3. 针对关键词或对话整体进行情绪分析，判断情绪为积极、中性或消极，并给出相应情绪描述或得分。
4. 请按照下面的 JSON 格式输出结果，输出内容中不得包含其他非 JSON 的文字，确保输出可以直接保存到数据库中。

输入文本：{conversation}

输出格式要求：

{{
    "keywords": [
        {{
            "keyword": "关键词1",
            "frequency": 数值,
            "emotion": "积极/中性/消极"
        }},
        {{
            "keyword": "关键词2",
            "frequency": 数值,
            "emotion": "积极/中性/消极"
        }},
        ……
    ]
}}

"""


# ########################################### VLLM相关参数 #######################################

CONSULT_VLLM_CASE_TEMPLATE = """
你是一位专业医学助理和文档识别专家。

我将上传一张医院病例图片，内容来自不同医院，结构不固定，可能包含患者信息、诊断记录、检验结果、医生建议等内容。

请以OCR方式识别图片中的全部文字内容，要求：
- 内容完整、专业；
- 保留原有医学术语、字段、表述；
- 遵循自然阅读顺序（从上到下、从左到右）；
- 忽略图像中不清晰或无法识别的部分；
- 不要做总结或分析。

请开始识别。
"""
