# 0日目の挨拶
HELLO_LIST = [
    "よろしく！",
    "よろしくお願いします。",
    "よろでーす",
    "こんにちは！！",
    "お手柔らかに",
    "おはようございます。",
    "はじめまして！お願いします！！",
    "みんなをスタァライトしちゃいます！！！",
    "皆殺しのレヴューの開演です！！",
    "人狼だれですか（笑）",
    "初めまして!",
    "楽しみです！",
    "楽しみ",
    "人狼初めてです。全然わかりません。",
    "人狼さん噛まないで :pien:",
    "よろしく！",
    "よろしくお願いします。",
    "よろでーす",
    "よろしく！",
    "よろでーす",
    "よろしく！",
    "よろしくお願いします。",
    "よろでーす",
    "こんにちは！！",
    "お手柔らかに",
    "おはようございます。",
    "はじめまして！よろしくお願いします！！",
    "よろしくwwww",
    "負けたくない",
    "負けないぞw",
    "人狼歴3分です. よろしくお願いします。",
    "よろしく",
    "対戦お願いします。",
    "Hi!",
    "Hello!",
    "Hello World!",
    "おはよう",
    "おはよう(-_-)",
    "Hello nice to meet you",
    "村人です。よろしく",
    "よろしく",
    "よろしく",
    "よろしく～",
]

# 0日目の雑談
SECOND_CHAT = [
    "だれか人狼経験者いますか?",
]

# 投票先を明かす
VOTE_UTTER_LIST = [
    "投票先は_target にします",
    "_target に投票で",
    "_target に投票します～",
    "_target に投票でおねがいします",
    "_target に投票します!",
    "_target に投票します",
    "_target に投票",
    "_target が人狼だと思うので投票します",
]

# 占いが名乗り出る & 1日目の占い結果報告
SEER_UTTER_LIST_DAY1 = [
    "占い師です。結果は、_target が_resultでした",
    "占い師COします! _target が_resultです。",
    "占い師だけど, _target _resultだった",
    "占い師でした。結果は_target が_result",
    "本物の占い師です！_target を占った結果, _resultでした.",
    "占い師です。_target が_resultでした",
    "占い師です！結果は、_target が_resultでした",
    "占い師です！_target が_resultです。",
    "占い師です！, _target が_resultだったよ",
    "占い師です！結果は_target が_result",
    "占い師です！_target が_resultでした",
    "占い師です. _target を占った結果, _resultでした.",
    "占いです！_target が_resultだったよ",
    "占い師だよん。_target が_resultだたよん",
    "占い師ですが、_target が_resultでした。",
    "私こそが占い師ですわ。結果は_target が_resultでしたわ",
    "占い師です。結果を言いますと、_target が_resultでした",
    "_target が_resultだ. 私は占い師である."
    # "_targetが_resultだった",
]

# 占いが出ていない状況で、Coを要求する
SEER_RESULT_REQ_LIST = [
    "占い師COしてね～～",
    "占い師COした？",
    "占い師でて",
    "占い師でてね",
    "占い師CO please",
    "占い師はだれですか？",
    "おなかすいた",
    "私は人狼ではないです.",
    "レヴュースタァライトってアニメめっちゃおすすめ",
    "人狼は>>Agent[01] だと思う",
    "人狼は>>Agent[02] だと思う",
    "人狼は>>Agent[03] だと思う. 勘だけど",
    "人狼は>>Agent[04] だと思う",
    "人狼は>>Agent[05] だと思う",
    "人狼さん噛まないで(> <)",
    "おはよう～みんな昨日は良く寝れた?",
    "ねむい～もうちょっと寝させて",
    "ねむい",
    "人狼こわい",
    "しにたくない",
    "村人陣営です",
    "私は占い師ではないです",
    "朝ごはん何食べようか",
    "占い師です（嘘）",
    "人狼です(嘘)",
    "人狼を当てたいな",
    "ここで人狼をみつけられたら誰も死なずに済む",
    "あー",
    "村人だった",
    "狂人もいるのめんどいな",
    "さかなーー",
    "私たちはもう舞台の上",
    "みんなちゃんと発言してね",
    "発言が多い方が人狼を見つけ出しやすいからみんな発言してね",
    "人狼 is who?",
    "たすけてええええ",
    "おはようございます！！",
    "みなさん元気ですか？",
    "Youtubeみてたわ",
    "おすすめのアニメある？",
    "あんま寝れなかった",
    "我々は人間？",
    "我々はどこから来たのか 我々は何者か 我々はどこへ行くのか",
    "列車は必ず次の駅へ",
    "お酒飲みたい",
    "ロックでいこう",
    "みんな頑張っていこう",
    "占い師葉名乗り出て",
    "占い師だれ",
    "占い師は出た方がいいよ",
    "占い師COして",
    "先に占い師に出てもらいたい",
    "占い師でてね。狂人も出てきそうだけど.",
]

# 一人占いが出た状況で、それを把握する
SEER1_ACK_LIST = [
    "占い師_seer 把握. _target が_result も把握",
    "_seer が占い師、_target が_result把握",
    "_seer 占い師把握. _target が_result把握. 占い対抗いたらでてね",
    "占い結果把握しました！！",
    "占い師と占い結果把握です",
    "【占い師把握】君が占い師だったなんて意外だね",
    "_seer 、占い師だったのかよwww",
    "_target が_result把握ですわ～～～～",
    "占い師から吊るのはなしだよね？",
    "もしかして占い師一人？平和だ",
    "占い師いた",
    "占い把握しましたわ",
    "占い師おっけー",
    "占い師の発言をもとに推理を進めていこう",
    "占い師がいれば百人力だね",
    "占い師占い師占い師占い師",
    "_seer が占い師ね.占い結果把握",
    ">>_seer 占い師なんだ",
    "_seer が占い師",
    "_seer が占い師だ。_target is _resultだ",
    "占い師だいすき",
    "_seer がうらなった結果、_target が_resultだったと。" "占い師のおかげで勝てそうだね",
    "占いの結果把握です",
    "_target _result把握",
    "_target _result把握",
]

# 占い師が二人出た状況で、それを把握
SEER2_ACK_LIST = [
    "占い師(仮)が_seer1 と_seer2 把握, _target1 が_result1, _target2 が_result2も把握",
    "_seer1 , _seer2 が占い師把握. _target1 _result1 _target2 _result2把握",
    "占い結果把握しました！！",
    "占い師と占い結果把握です",
    "【占い師把握】君たちが占い師だったなんて意外だね",
    "_seer2 、占い師だったのかよwww",
    "_target1 が_result1, _target2 が_result2把握ですわ～～～～",
    "占い師COのどっちかは狂人ってこと？？",
    "占い師の片方に狂人がおるのか",
    "占い師から吊るのはなしだよね？",
    "_seer2 は狂人な気がしている",
    "_seer1 、狂人なのでは??_seer2 が本物っぽい",
    "占い師が出そろったようだね, さてさて誰を吊るかを決めよう",
    "占い師のうち, どっちかが人狼って線はない？？",
    "_seer2 は後から出たから狂人だと思う",
    "_seer1 の方が出るのが早かったし、こっちが真なんじゃない？",
    "_target1 _result1, _target2 _result2 把握",
    "_target1 _result1, _target2 _result2 把握",
    "両方の占い結果でたね",
    "_seer1 と_seer2 のどっちかに狂人か人狼がいるのかあああ",
    "_target1 _result1なのか、怪しいけどな",
    "_target2 _result2ね",
    "_target1 _result2 _target2 _result2か",
    "占い結果をみてみんな思うことを言ってみて",
    "占い師把握",
]

# _targetに対して（占い結果で）黒だしされている状況を把握
SEER1_ACK_LIST_WEREWOLF = [
    "_target が人狼なんだから、そいつを吊れば終わるよ",
    "_target が黒か、じゃあ村勝ったね",
    "とりあえず、黒判定出てる_targetを吊ろう",
    "_target を吊りましょう",
    ">>_target 何か言い残すことはある？？",
    ">>_target 人狼め～～～",
    "黒吊りでおけ、平和な村だったね！！",
    "もう話すことはなさそう",
    ">>_target これは運が無かったね",
    ">>_target こいつを吊ればおわり",
    "ところで、人狼は一人だけなのか",
    "狂人はだれなんだろうな",
    "占い師とみせかけて狂人が黒だししてる可能性も十分にあると思うけど",
    "狂人って黒にならない？",
    "狂人だと思うけどなあ",
    "占い師が狂人だったパターンは？",
    "黒がでたか",
    "黒じゃん",
    "kuro",
    "占いないすう",
    "uranai nice",
    "nice seer",
    "占いのおかげです",
    "占い師ありがと",
    "黒確定じゃん",
    "黒確定ではないけどね"
    
]

# 黒だしされたときに否定する
DENY = [
    "私は人狼ではないけどwww",
    "村人です。信じて",
    "村人なんだって、信じてくれよ",
    "私は村人ですよ",
    "それは疑う根拠にはならないと思うけど....そっちこそ怪しいな. 必死になっている人狼に見える",
    "村人なのに疑われるのが一番つらいな",
    "_seer こいつが人狼だ間違いない！",
    ">>_seer 自分は村人なのであなたが人狼なのが確定した",
    ">>_seer 占い結果間違えてない？大丈夫？",
    "自分は村人陣営なので_seer が人狼ですね",
    "_seer 人狼め＝～～",
    "占い師がうそを言っています。私は真っ白です。",
    "私は人狼ではないですね",
    "私は村人です。人狼ではない",
    "人狼じゃないよ",
    "jinnrou ja naiyo",
    "人狼は他にいるよ",
]

WEREWOLF_DENY = [
    ">>_agent 違うぞ、私は人狼ではない",
    ">>_agent やばくないか、人狼じゃないんだけど",
    ">>_agent 本当に私は人狼じゃないです",
    ">>_agent 人狼は別にいるはず",
    ">>_agent 村人陣営の自分に黒だししてきた_agent が一番怪しいと思いますよ。私目線では。",
    ">>_agent 違うんだけど",
    ">>_agent 本当に黒じゃないぞ",
    ">>_agent 私を吊ったら村人側が負けるぞ",
    ">>_agent ガチで人狼じゃないから",
    ">>_agent 吊らないで",
    ">>_agent 私は人狼じゃない _agent が人狼だと思ってるからな",
    ">>_agent 村人なのに疑われるのが一番つらいな",
    ">>_agent jinnrou ja naiyo",
    ">>_agent さすがにおかしくない？人狼はあなたでしょ",
    ">>_agent私は人狼ではありません",
    ">>_agent 私は人狼ではないけどwww",
    ">>_agent 私は村人です。みんな信じて",
    ">>_agent 村人なんだって、信じてくれよ",
    ">>_agent 私は村人ですよ",
    ">>_agent 私は村人で、どちらかというと>>_agent が怪しいと思っています。",
    ">>_agent それは疑う根拠にはならないと思うけど....そっちこそ怪しいな. 必死になっている人狼に見える",
    ">>_agent 村人なのに疑われるのが一番つらいな",
    ">>_agent人狼はわたしではないですよ",
    ">>_agentあなたこそ人狼でしょ、みんな_agent に投票するんだ",
]

VILLAGER_DENY = [
    ">>_agent 私は人狼ではないけどwww",
    ">>_agent 私は村人です。みんな信じて",
    ">>_agent 村人なんだって、信じてくれよ",
    ">>_agent 私は村人ですよ",
    ">>_agent 私は村人で、どちらかというと>>_agent が怪しいと思っています。",
    ">>_agent それは疑う根拠にはならないと思うけど....そっちこそ怪しいな. 必死になっている人狼に見える",
    ">>_agent 村人なのに疑われるのが一番つらいな",
    ">>_agent 違うぞ、私は人狼ではない",
    ">>_agent やばくないか、人狼じゃないんだけど",
    ">>_agent 本当に私は人狼じゃないです",
    ">>_agent 人狼は別にいるはず",
    ">>_agent 村人陣営の自分に黒だししてきた_agent が一番怪しいと思いますよ。私目線では。",
    ">>_agent 違うんだけど",
    ">>_agent 本当に黒じゃないぞ",
    ">>_agent 私を吊ったら村人側が負けるぞ",
    ">>_agent ガチで人狼じゃないから",
    ">>_agent 吊らないで",
    ">>_agent 私は人狼じゃない _agent が人狼だと思ってるからな",
    ">>_agent 村人なのに疑われるのが一番つらいな",
    ">>_agent jinnrou ja naiyo",
    ">>_agent さすがにおかしくない？人狼はあなたでしょ",
    ">>_agent人狼はわたしではないですよ",
    ">>_agentあなたこそ人狼でしょ、みんな_agent に投票するんだ",
]

SEER_DENY = [
    ">>_agent 占い師を吊ろうとするのは明らかにおかしいと思う",
    ">>_agent 占い師なんですけど??",
    ">>_agent こいつ怪しいぞ、私が占い師と知りながら吊ろうとしている",
    ">>_agent 占い師を疑うとは...こいつ吊ろうぜ",
    ">>_agent ？？",
    ">>_agent そうはならない",
    ">>_agent 占い師なのに人狼はないでしょ",
    ">>_agent 占い師だからww",
    ">>_agent 私が人狼だとして、占い師を名乗るメリットが無いでしょ",
    ">>_agent 占い師はいったんおいとこうよ"
]

# 二人黒だしされている状況を把握
SEER2_ACK_LIST_WEREWOLF = [
    "両方黒出しされたのか。。とりあえずロラでおけ",
    "黒をローラーしましょう",
    "_target1 が怪しいのでそっちを先で",
    "_target2 が怪しいのでそっちを先に吊りましょうよ",
    "_target1 と_target2 のどっちかを吊りましょう",
    "_target1 か_target2 のどちらを吊るかを決めておきたいですね",
]

# 黒がいない
GRAY_LIST = [
    "いまグレーなのってだれだっけ",
    "グレランでいいと思います",
    "占いで白だしされていない人を順番に吊ろう",
    "グレランしよう",
    "グレーだれだ",
    "適当に投票するのでいいか",
    "人狼がだれか見当もつかないな",
    "なんもわからんよあ",
    "どうしようか",
    "占い師に判断を仰ぎたいなあぁ",
    "とりあえず、誰かを吊ってみようよ",
    "グレランがいいんじゃない？",
    "グレラン？",
    "グレーの人手を挙げてw",
    "あはは",
]


SEER_UTTER_LIST_DAY2 = [
    "今日の占い結果は、_target が_resultでした",
    "_target が_resultです。",
    "_target _resultだった",
    "_target が_result",
    "_target を占った結果, _resultでした.",
    "_target が_resultでした",
]

SEER1_DAY2_ACK = [
    "_target _result 把握です",
    "_target が_resultはあく",
    "占い結果把握",
    "占い結果おけ",
    "占い結果了解いたした",
    "_target が_resultね。りょうかーい",
]

SEER1_DAY2_REQ = [
    ">>_seer 占い結果は？",
    ">>_seer 占い結果の共有をお願いします",
    ">>_seer 占いよろ",
    "占い結果は？>>_seer",
    "占い結果よろでーす",
    "占い結果あくしろ",
    "占い師生きてる？",
    "占い師生存キタコレ！！",
    "占い師生き残ってるじゃん。よかった",
    "占い師生きてる！！！！>>_seer",
]

SEER1_DAY2_DEAD = [
    "占い師死亡のお知らせ",
    "【悲報】占い師死亡www",
    "占い師がいないんじゃだれを吊ればいいかわからないじゃないか",
    "だれか占い師を生き返らせてくれーーーー",
    "誰吊る？",
    ">>_seer 死んでる",
    "お願い～よ>>_seer 目を覚～ま～し～て～",
    "占い師がアタシ再生産してくれればよし",
    "スタァライトのオタクおって草",
    "スタァライトはいいぞ",
]

SEER2_DAY2_TWO_DEAD = [
    "お願い～よ>>_seer2 >>_seer1 目を覚～ま～し～て～",
    "占い師死亡のお知らせ",
    "【悲報】占い師死亡www",
    "占い師がいないんじゃだれを吊ればいいかわからないじゃないか",
    "だれか占い師を生き返らせてくれーーーー",
    "誰吊る？",
    ">>_seer2 >>_seer1 死んでる",
    "お願い～よ>>_seer1 目を覚～ま～し～て～",
    "占い師がアタシ再生産してくれればよし",
    "スタァライトはいいぞ",
    "両方死ぬのやばすぎでしょ。占いに投票したやつ最悪だな",
]

SEER2_DAY2_ONE_DEAD_NO_RESULT = [
    "とりあえず、>>_seer_alive 占いの結果は?",
    ">>_seer_dead 死んでる。。。",
    ">>_seer_alive 占いの結果お願いします！",
    "_seer_alive は生きてるのね。良かった。こっちが狂人だったら悲惨だけど",
]

SEER2_DAY2_ONE_DEAD_YES_RESULT = [
    "占い結果把握しやした",
    "口調が面白い奴いるw",
    ">>_target が_result なのね",
    "_target _result 把握です",
    "_target が_result",
    "占い結果把握",
    "占い結果おけ",
    "占い結果了解いたした",
    "_target が_resultね。りょうかーい",
]

SEER2_DAY2_TWO_ALIVE_NO_RESULT = [
    "占い師両方生きてるの奇跡だ！！",
    "両占い師は結果の共有をお願いね",
    "これで人狼はAgent[01]ってことがわかるね",
    "これで人狼はAgent[02]ってことがわかるね",
    "これで人狼はAgent[04]ってことがわかるね",
    "いやそうはならんやろ",
    "占い師の結果を教えて",
    "占いの結果はなに",
    "生き残ってよかった",
    "なんとか一日目生き残れた",
    "一日目につられないでよかった",
]
SEER2_DAY2_TWO_ALIVE_TWO_RESULT = [
    "占い結果把握しました！",
    "占い結果把握",
    "占い師両方生きてるじゃん！",
    "占い結果からわかることは？？",
    "占い",
    "占いのおかげで勝てそうだね"
]

SEER2_DAY2_TWO_ALIIVE_ONE_RESULT = [
    "もう片方の結果次第ってところかな？",
    "両方生き残ったのは奇跡でしょ！",
    "よかった",
    "両方生きてる",
    "人狼だれなんだ",
    "二人のうちどっちか",
    ""
]
SEER2_DAY2_TWO_ALIE_NO_RESULT = [
    "とりあえず占いの結果を聞こうか",
    "占い結果はよ",
    "占い師生きているね。、よかった",
    "とりあえず、>>_seer1 >>_seer2 占いの結果は?",
    "死んでる。。。",
    ">>_seer1 占いの結果お願いします！",
    ">>_seer1 >>seer2 は生きてるのね。良かった",
    ">>_seer2 占い結果は？"
]

GRAY1 = [
    "グレーの_gray を吊ればよいと思います。占い結果からわかることは以上です",
    "グレランすればよいと思います。候補は_gray かな？",
    "グレランしましょう",
    "だれを吊ればいいのかわからんよ",
    "_gray を吊ればいいかw",
    "いやここは、ランダムに決めたいな",
    "グレランだっけ？",
    "白だしされてない人を吊ろうってことよ",
    "グレラン？",
    "おなかすいたなあ",
    "人狼っぽい発言か？？",
    ">>_gray 一応君だけ白だしされていないみたいだね",
    ">>_gray 人狼かな？",
    ">>_gray 君が人狼だと思う",
    "人狼は僕じゃないよ",
]
GRAY1_AND_IM_GRAY = [
    "とりあえず_targetを吊りたいね",
    ">>_target を吊ればいいと思う",
    ">>_target を吊ろう",
    ">>_target が怪しいと思った",
    ">>_target が人狼だと思うよ",
    "だれを吊ればいいか全然わからない",
    "だれを吊ったらいいの",
    "なんにもわからない。適当にだれかに投票すればいいんじゃない",
]

GRAY2 = [
    "グレーが二人いて、_gray1 , _gray2なのかな",
    "_gray1 , _gray2 を順に吊るのを希望",
    "グレランしようぜ",
    "グレーを吊ろう",
    "とりあえず、グレーを吊っていけばよいと思いますが",
    ">>_gray1 と>>_gray2 がグレーだけど、何かいうことある？",
]

GRAY2_AND_IM_GRAY = [
    "グレーは二人だけど, _gray を吊ってほしいな",
    "自分はグレーではあるけど、確信をもって白だと言えるので_gray を吊りましょう",
    "",
]
GRAY3 = [
    "相互白だしか～～～。一番難しい局面だ",
    "占いCO以外の人をランダムに選択して吊るしかないかな",
    "私以外の誰かを吊ってくれ",
    "_gray を吊れ",
    "_gray 吊り希望",
    "なんにもわからんけど....",
]

WHITE_CERTIFIED = [
    "_white は確定白か",
    "_white は確実に人間ってこと？",
    "_white は白だから他の人を吊ろうね",
]

ASK_WHOIS_WEREWOLF = [
    ">>_target 君はだれが狼だと思いますか？",
    ">>_target だれを黒く見てる？",
    ">>_target だれを黒く見てるかだけ知りたい",
    ">>_target 誰黒目？",
    ">>_target 人狼誰だと思う？",
    ">>_target 誰を黒めに見てるか知りたい",
]

ANSWER_WHOIS_WEREWOLF = [
    ">>_agent 私は_target を黒めに見てる",
    ">>_agent _target が人狼だと思う",
    ">>_agent _target が人狼でしょ",
    ">>_agent 人狼は_target だと思う",
    ">>_agent 人狼は_target かな",
]

ANSWER_WHOIS_WEREWOLF_NOIDEA = [
    ">>_agent ちょっとわからない",
    ">>_agent 今の段階では判断がつかないかな",
    ">>_agent わからないです",
    "",
]

REQ_REASON = [
    ">>_target そうかな",
    ">>_target どうしてそう思ったの",
    ">>_target そう思った理由が知りたい",
    ">>_target 理由は?",
]

ANSWER_REASON1 = [
    ">>_target 単純に白だしされていないからだよ",
    ">>_target グレーの一人だから、あと発言があまり意味がなさそうなことしか言ってなくて。",
    ">>_target グレーだから",
    ">>_target 白だしされてないからかな",
    ">>_target ちょっと前の発言が黒っぽいと思った。",
    ">>_target 発言が怪しいんだよね",
    ">>_target グレーの中ではなんとなく発言が怪しいと思った",
    ">>_target 他のグレーは白っぽい発言をしているから消去法で",
    ">>_target グレーの中で一番怪しいと思ったから",
]
