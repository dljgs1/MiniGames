var events_c12a15a8_c380_4b28_8144_256cba95f760 = 
{
	"commonEvent": {
		"加点事件": [
			{
				"type": "comment",
				"text": "通过传参，flag:arg1 表示当前应该的加点数值"
			},
			{
				"type": "choices",
				"choices": [
					{
						"text": "攻击+${1*flag:arg1}",
						"action": [
							{
								"type": "setValue",
								"name": "status:atk",
								"operator": "+=",
								"value": "1*flag:arg1"
							}
						]
					},
					{
						"text": "防御+${2*flag:arg1}",
						"action": [
							{
								"type": "setValue",
								"name": "status:def",
								"operator": "+=",
								"value": "2*flag:arg1"
							}
						]
					},
					{
						"text": "生命+${200*flag:arg1}",
						"action": [
							{
								"type": "setValue",
								"name": "status:hp",
								"operator": "+=",
								"value": "200*flag:arg1"
							}
						]
					}
				]
			}
		],
		"回收钥匙商店": [
			{
				"type": "comment",
				"text": "此事件在全局商店中被引用了(全局商店keyShop)"
			},
			{
				"type": "comment",
				"text": "解除引用前勿删除此事件"
			},
			{
				"type": "comment",
				"text": "玩家在快捷列表（V键）中可以使用本公共事件"
			},
			{
				"type": "while",
				"condition": "1",
				"data": [
					{
						"type": "choices",
						"text": "\t[商人,trader]你有多余的钥匙想要出售吗？",
						"choices": [
							{
								"text": "黄钥匙（10金币）",
								"color": [
									255,
									255,
									0,
									1
								],
								"action": [
									{
										"type": "if",
										"condition": "item:yellowKey >= 1",
										"true": [
											{
												"type": "setValue",
												"name": "item:yellowKey",
												"operator": "-=",
												"value": "1"
											},
											{
												"type": "setValue",
												"name": "status:money",
												"operator": "+=",
												"value": "10"
											}
										],
										"false": [
											"\t[商人,trader]你没有黄钥匙！"
										]
									}
								]
							},
							{
								"text": "蓝钥匙（50金币）",
								"color": [
									0,
									0,
									255,
									1
								],
								"action": [
									{
										"type": "if",
										"condition": "item:blueKey >= 1",
										"true": [
											{
												"type": "setValue",
												"name": "item:blueKey",
												"operator": "-=",
												"value": "1"
											},
											{
												"type": "setValue",
												"name": "status:money",
												"operator": "+=",
												"value": "50"
											}
										],
										"false": [
											"\t[商人,trader]你没有蓝钥匙！"
										]
									}
								]
							},
							{
								"text": "离开",
								"action": [
									{
										"type": "exit"
									}
								]
							}
						]
					}
				]
			}
		],
		"Guide": [
			{
				"type": "switch",
				"condition": "flag:arg1",
				"caseList": [
					{
						"case": "'gift'",
						"action": [
							"\t[提示]怪物成功融合可以获取金币",
							"\t[提示]每当金币获取一定数额后 将会获取奖励\n下次所需的金币以及奖励物品将在状态栏提示",
							{
								"type": "comment",
								"text": "当判别值是值的场合执行此事件"
							}
						]
					},
					{
						"case": "'first'",
						"action": [
							"\t[提示]同种怪物在推击接近后 将会合并成更强的怪物",
							"\t[提示]每过一回合 掉落一个怪物\n可以通过推击打消耗回合 也可以使用背包中的\\i[freezeBadge] \n下一次坠落的怪物 将会以半透明提示",
							"\t[提示]更多疑问可以点开背包的\\i[I320]说明书。",
						]
					},
					{
						"case": "'shop1'",
						"action": [
							"\t[提示]金币商店已启用，按V或者点击\\i[shop]打开。",
							{
								"type": "openShop",
								"id": "shop1",
								"open": true
							}
						]
					},
					{
						"case": "'shop2'",
						"action": [
							"\t[提示]道具商店已启用，按V或者点击\\i[shop]打开。",
							{
								"type": "openShop",
								"id": "itemShop",
								"open": true
							}
						]
					}
				]
			}
		]
	}
}