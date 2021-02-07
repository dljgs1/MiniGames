var data_a1e2fb4a_e986_4524_b0da_9b7ba7c0874d = 
{
	"main": {
		"floorIds": [
			"MT0",
			"ET"
		],
		"floorPartitions": [],
		"images": [
			"bg.jpg",
			"hero.png",
			"winskin.png"
		],
		"tilesets": [
			"magictower.png"
		],
		"animates": [
			"hand",
			"sword",
			"zone"
		],
		"bgms": [
			"bgm.mp3"
		],
		"sounds": [
			"floor.mp3",
			"attack.mp3",
			"door.mp3",
			"item.mp3",
			"equip.mp3",
			"zone.mp3",
			"jump.mp3",
			"pickaxe.mp3",
			"bomb.mp3",
			"centerFly.mp3",
			"combine.mp3",
			"gift.mp3"
		],
		"fonts": [],
		"nameMap": {
			"背景图.jpg": "bg.jpg",
			"背景音乐.mp3": "bgm.mp3"
		},
		"levelChoose": [],
		"equipName": [
			"武器",
			"盾牌"
		],
		"startBgm": null,
		"styles": {
			"startBackground": "project/images/bg.jpg",
			"startVerticalBackground": "project/images/bg.jpg",
			"startLogoStyle": "color: white",
			"startButtonsStyle": "background-color: #32369F; opacity: 0.85; color: #FFFFFF; border: #FFFFFF 2px solid; caret-color: #FFD700;",
			"statusLeftBackground": "url(project/materials/ground.png) repeat",
			"statusTopBackground": "url(project/materials/ground.png) repeat",
			"toolsBackground": "url(project/materials/ground.png) repeat",
			"floorChangingStyle": "background-color: black; color: white",
			"statusBarColor": [
				255,
				255,
				255,
				1
			],
			"borderColor": [
				204,
				204,
				204,
				1
			],
			"selectColor": [
				255,
				215,
				0,
				1
			],
			"font": "Verdana"
		}
	},
	"firstData": {
		"title": "寻找魔王",
		"name": "combineKing",
		"version": "Ver 2.7.3.1",
		"floorId": "MT0",
		"hero": {
			"image": "hero.png",
			"animate": false,
			"name": "阳光",
			"lv": 1,
			"hpmax": 9999,
			"hp": 10000,
			"manamax": -1,
			"mana": 0,
			"atk": 10,
			"def": 10,
			"mdef": 0,
			"money": 0,
			"exp": 0,
			"equipment": [],
			"items": {
				"constants": {
					"book": 1,
					"freezeBadge": 1,
					"I320": 1
				},
				"tools": {},
				"equips": {}
			},
			"loc": {
				"direction": "up",
				"x": 6,
				"y": 10
			},
			"flags": {
				"force": 5,
				"forceMul": 1
			},
			"followers": [],
			"steps": 0
		},
		"startCanvas": [
			{
				"type": "comment",
				"text": "在这里可以用事件来自定义绘制标题界面的背景图等"
			},
			{
				"type": "comment",
				"text": "也可以直接切换到其他楼层（比如某个开始剧情楼层）进行操作。"
			},
			{
				"type": "showImage",
				"code": 1,
				"image": "bg.jpg",
				"loc": [
					0,
					0
				],
				"opacity": 1,
				"time": 0
			},
			{
				"type": "while",
				"condition": "1",
				"data": [
					{
						"type": "comment",
						"text": "给用户提供选择项，这里简单的使用了choices事件"
					},
					{
						"type": "comment",
						"text": "也可以贴按钮图然后使用等待操作来完成"
					},
					{
						"type": "choices",
						"choices": [
							{
								"text": "开始游戏",
								"action": [
									{
										"type": "comment",
										"text": "检查bgm状态，下同"
									},
									{
										"type": "function",
										"function": "function(){\ncore.control.checkBgm()\n}"
									},
									{
										"type": "if",
										"condition": "main.levelChoose.length == 0",
										"true": [
											{
												"type": "comment",
												"text": "直接开始游戏"
											}
										],
										"false": [
											{
												"type": "comment",
												"text": "动态生成难度选择项"
											},
											{
												"type": "function",
												"function": "function(){\nvar choices = [];\nmain.levelChoose.forEach(function (one) {\n\tchoices.push({\n\t\t\"text\": one.title || '',\n\t\t\"action\": [\n\t\t\t{ \"type\": \"function\", \"function\": \"function() { core.status.hard = '\" + (one.name || '') + \"'; }\" }\n\t\t]\n\t});\n})\ncore.insertAction({ \"type\": \"choices\", \"choices\": choices });\n}"
											}
										]
									},
									{
										"type": "hideImage",
										"code": 1,
										"time": 0
									},
									{
										"type": "comment",
										"text": "成功选择难度"
									},
									{
										"type": "break"
									}
								]
							},
							{
								"text": "读取存档",
								"action": [
									{
										"type": "function",
										"function": "function(){\ncore.control.checkBgm()\n}"
									},
									{
										"type": "comment",
										"text": "简单的使用“呼出读档界面”来处理"
									},
									{
										"type": "callLoad"
									}
								]
							},
							{
								"text": "回放录像",
								"action": [
									{
										"type": "function",
										"function": "function(){\ncore.control.checkBgm()\n}"
									},
									{
										"type": "comment",
										"text": "这段代码会弹框选择录像文件"
									},
									{
										"type": "if",
										"condition": "(!core.isReplaying())",
										"true": [
											{
												"type": "function",
												"function": "function(){\ncore.chooseReplayFile()\n}"
											}
										]
									}
								]
							}
						]
					}
				]
			},
			{
				"type": "comment",
				"text": "接下来会执行startText中的事件"
			}
		],
		"startText": [
			"魔塔倒塌后，魔王使用天魔解体化成一片妖雾，飘到了上空。\n现在天上开始下怪物了，这些怪物都无法被击败，你要去融合它们，找到魔王。"
		],
		"shops": [
			{
				"id": "shop1",
				"text": "\t[贪婪之神,moneyShop]勇敢的武士啊, 给我${20+20*flag:shop1}金币就可以：",
				"textInList": "金币商店",
				"mustEnable": false,
				"disablePreview": false,
				"choices": [
					{
						"text": "生命+800",
						"need": "status:money>=20+20*flag:shop1",
						"action": [
							{
								"type": "comment",
								"text": "新版商店中需要手动扣减金币和增加访问次数"
							},
							{
								"type": "setValue",
								"name": "status:money",
								"operator": "-=",
								"value": "20+20*flag:shop1"
							},
							{
								"type": "setValue",
								"name": "flag:shop1",
								"operator": "+=",
								"value": "1"
							},
							{
								"type": "setValue",
								"name": "status:hp",
								"operator": "+=",
								"value": "800"
							}
						]
					},
					{
						"text": "攻击+4",
						"need": "status:money>=20+20*flag:shop1",
						"action": [
							{
								"type": "comment",
								"text": "新版商店中需要手动扣减金币和增加访问次数"
							},
							{
								"type": "setValue",
								"name": "status:money",
								"operator": "-=",
								"value": "20+20*flag:shop1"
							},
							{
								"type": "setValue",
								"name": "flag:shop1",
								"operator": "+=",
								"value": "1"
							},
							{
								"type": "setValue",
								"name": "status:atk",
								"operator": "+=",
								"value": "4"
							}
						]
					},
					{
						"text": "防御+3",
						"need": "status:money>=20+20*flag:shop1",
						"action": [
							{
								"type": "setValue",
								"name": "status:money",
								"operator": "-=",
								"value": "20+20*flag:shop1"
							},
							{
								"type": "setValue",
								"name": "flag:shop1",
								"operator": "+=",
								"value": "1"
							},
							{
								"type": "setValue",
								"name": "status:def",
								"operator": "+=",
								"value": "3"
							}
						]
					}
				]
			},
			{
				"id": "itemShop",
				"item": true,
				"textInList": "道具商店",
				"mustEnable": false,
				"choices": [
					{
						"id": "cross",
						"number": 1,
						"money": "35",
						"sell": "5"
					},
					{
						"id": "lifeWand",
						"number": 10,
						"money": "100",
						"sell": "5"
					},
					{
						"id": "superWine",
						"number": 99,
						"money": "5",
						"sell": "5"
					},
					{
						"id": "sword0",
						"number": 5,
						"money": "100",
						"sell": "5"
					},
					{
						"id": "dagger",
						"number": 50,
						"money": "10",
						"sell": "5"
					}
				]
			}
		],
		"levelUp": [
			{
				"need": "0",
				"title": "",
				"action": [
					{
						"type": "comment",
						"text": "此处是初始等级，只需填写称号"
					}
				]
			},
			{
				"need": "20",
				"title": "",
				"action": [
					{
						"type": "setValue",
						"name": "status:atk",
						"operator": "+=",
						"value": "10"
					},
					{
						"type": "setValue",
						"name": "status:def",
						"operator": "+=",
						"value": "10"
					}
				]
			},
			{
				"need": "40",
				"title": "",
				"action": [
					{
						"type": "tip",
						"text": "恭喜升级"
					}
				]
			}
		]
	},
	"values": {
		"lavaDamage": 100,
		"poisonDamage": 10,
		"weakValue": 20,
		"redGem": 1,
		"blueGem": 1,
		"greenGem": 2,
		"redPotion": 50,
		"bluePotion": 100,
		"yellowPotion": 200,
		"greenPotion": 300,
		"breakArmor": 0.9,
		"counterAttack": 0.1,
		"purify": 3,
		"hatred": 2,
		"animateSpeed": 400,
		"statusCanvasRowsOnMobile": 3,
		"floorChangeTime": 500,
		"combineGift": {
			"smallThr": 10,
			"midThr": 23,
			"bigThr": 42,
			"smallList": [
				31,
				32
			],
			"midList": [
				27,
				28,
				29
			],
			"bigList": [
				34,
				33,
				30
			]
		}
	},
	"flags": {
		"statusBarItems": [
			"enableFloor",
			"enableHP",
			"enableAtk",
			"enableDef",
			"enableMDef",
			"enableMoney",
			"enableKeys"
		],
		"flyNearStair": true,
		"flyRecordPosition": false,
		"steelDoorWithoutKey": false,
		"itemFirstText": false,
		"equipboxButton": false,
		"enableAddPoint": false,
		"enableNegativeDamage": false,
		"betweenAttackMax": false,
		"useLoop": false,
		"startUsingCanvas": false,
		"statusCanvas": true,
		"displayEnemyDamage": true,
		"displayCritical": true,
		"displayExtraDamage": true,
		"enableGentleClick": true,
		"ignoreChangeFloor": true,
		"canGoDeadZone": false,
		"enableMoveDirectly": true,
		"enableRouteFolding": true,
		"disableShopOnDamage": false,
		"blurFg": false
	}
}