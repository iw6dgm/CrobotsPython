class Configuration(object):
    label = 'koth'
    matchF2F = 200
    match3VS3 = 2
    match4VS4 = 1
    sourcePath = './f2f'
    listRobots = ['lamela', 'power', 'eternity', 'vector', 'john_blaze', 'ride', 'jumba', 'change', 'armin', 'gru',
                  'proud', 'gantu', 'suddenly', 'nustyle', 'vain', 'tantalo', 'confusion', 'revo', 'osvaldo', 'life',
                  'cvirus2', 'gerty3', 'ghostrider', 'okapi', 'jedi12', '!dna', 'angel', '!alien', '!zeus', 'crossover',
                  'cvirus', 'axolotl', 'aladino', 'macro1', 'colosso', 'guanaco', 'crazy96', 'pippo11b', 'jedi9',
                  'midi1', 'gotar', 'jedi8', 'wall-e_iv', 'lufthansa', 'leopon', 'party', 'rythm', 'iceman', 'hal9013',
                  'ug2k', 'wgdi', 'drizzt', 'virus2', 'virus3', 'druzil', 'reuben', 'virus4', 'british', 'ire',
                  'puffomac', 'alcadia', 'zorn', 'rudolf_8', 'virus', 'multics', 'destro', 'lycan', 'rudolf_x',
                  'harlock', 'rudolf_7', 'rudolf_9', 'z', 'unmaldestr', 'wulfgar', 'elminster', 'wall-e_iii', 'e',
                  'moveon', 'frankie', 'hal9012', 'puffomid', '!caos', 'jedi10', 'ncc-1701', 'nikita', 'easyjet', 'sky',
                  'microbo2', 'enigma', 'tobey', 'grendizer', 'proton', 'minion', 'guntank', '4ever', 'yerba', 'yeti',
                  'puffomic', 'incolla', 'hal9010', 'ryanair', 'taglia', 'pippo13a', 'danica', 'neutron', 'zigozago',
                  'asterix', 'flash8e', 'pippo12a', 'cancella', 'wall-e_ii', 'bruenor', 'tannhause', 'spaceman',
                  'gerty', 'pjanic', 'draka', 'jedi5', 'padawan', 'janick', 'jarvis', 'disco', 'pippo07b', 'doom2099',
                  'dampyr', 'obelix', 'jedi7', 'hal9011', 'gongolo', 'silversurf', 'niso', 'zombie', 'jedi11',
                  'rudolf_6', 'flash8c', 'b_selim', 'irpef', 'copia', 'nautilus', 'gerty2', 'electron', 'knt',
                  'cariddi', 'm_selim', 'q', 'boom2', 'jedi6', 'pippo12b', 'sith', 'cadderly', 'cyborg_2', 'mystica',
                  'regis', 'tempesta', '7di9', 'satana', 'stitch', 'dna', 'pippo10a', 'goofy', 'pippo04b', 'remus',
                  'touch', '730', 'fire', 'pippo04a', 'artu', 'pain', 'daryl', 'beat', 'frisa_13', 'lancia13', 'pippo3',
                  'copter_2', 'todos', 'tomahawk', 'vegeth', 'irap', 'groucho', 'microbo1', 'wall-e', 'microdna',
                  'mrsatan', 'rat-man', 'pippo07a', 'sirio', 'coeurl', 'merlino', 'vampire', 'bach_2k', 'ortona_13',
                  'bati', 'eurialo', 'kyash_3c', 'puma', 'idefix', 'gengis', 'magneto', 'cobra', 'ires', 't', 'tigre',
                  'medioman', 'coyote', 'sharp', 'ici', 'megazai', 'brontolo', 'ares2', 'poldo', 'nemo', 'falco',
                  'selim_b', 'new_mini', 'carlo2k', 'raistlin', 'pippo13b', 'pisolo', 'janu', 'stealth', 'ravatto',
                  'dnablack', 'sweat', 'pyro', 'elisir', 'dario', 'marko', 'pippo11a', 'rudy_xp', 'harris', 'red_wolf',
                  'maxicond', 'back', 'corner5', 'alien', 'romulus', 'unlimited', 'sharp2', 'gotar2', 'pippo2b', 'yoda',
                  'kyash_3m', 'mammolo', 'zifnab', 'smart', 'diodo', 'zener', 'colosseum', 'storm', 'bruce', 'fizban',
                  'panic', 'xeon', 'ciclope', 'jaja', 'coppi_2k', 'marine', 'ilbestio', 'burrfoot', 'dynacond', 'jeeg',
                  'mosfet', 'kakakatz', 'cyborg', 'fremen', 'stanlio', 'mancino', 'midi_zai', 'unico', 'rudolf_4',
                  'dynamite', 'songohan', 'fisco', 'rudolf_5', 'kongzill', 'ka_aroth', 'goblin', 'kyash_2', 'newzai17',
                  'adrian', 'dave', 'minicond', 'shock', 'dav2000', 'jedi3', 'pippo2a', 'homer', 'nl_5a', 'anakin',
                  'vibrsper', 'nl_3b', 'def2', 'scanner2', 'orione', 'carlo99', 'neo_sel', 'alfa99', 'pippo1b',
                  'alezai17', 'jedi4', 'flash5', 'omega99', 'adsl', 'tornado', '1_1', 'vauban', 'hal9005', 'pippo1a',
                  'nl_4b', 'origano', 'nl_4a', 'dav46', 'cancer', 'fable', 'defender', '_cimice_', 'digitale', 'pray',
                  'blitz', 'hal9004', 'jedi', 'leader', 'hammer', 'ataman', 'mind', 'rotar', 'scsi', 'borg', 'mister2b',
                  'cisc', 'camille', 'bartali', 'coppi', 'thunder2', 'beholder', 'theslayer', 'm_hingis', 'akira',
                  'ska', 'bastrd!!', 'freedom', 'mnl_1a', 'mazinga', 'jedi2', 'flash7', 'flash6', 'cliche', 'memories',
                  'copter', 'staticxp', 'nl_3a', 'sottolin', 'pippo3b', 'marlene', 'bigkarl', 'gostar', 'tartaruga',
                  'ollio', 'caccola', 'harpo', 'bjt', 'charles', 'kyashan', 'vision', 'nl_5b', 'barbarian', 'tequila',
                  'gers', 'diabolik', 'neo0', 'n3g4tivo', 'gunnyb13', 'pizarro', 'infinity', 'rudolf_3', 'poirot',
                  'new2', 'panduro', 'minatela', 'xabaras', 'quarto', 'huntlead', 'mnl_1b', 'carletto', 'drago6',
                  'obiwan', 'new', 'son-goku', 'serse', 'md9', 'quingon', 'aeris', 'minizai', 'dream', 'piiico',
                  'lazyii', 'politik', 'stay', 'zzz', 'attila', 'rudy', 'ares', 'kill!', 'zero', 'supernov', 'tox',
                  '11', 'drago5', 'colossus', 'hal9003', 'pippo93', 'athlon', 'ncmplt', 'mflash', 'b52', 'pentium4',
                  'murray', 'nl_1a', 'n3g4_jr', 'fya', 'pacoon', 'carlo97', 'md8', 'newb52', 'enkidu', 'rudolf',
                  'deluxe_3', 'rudolf_2', 'staticii', 'am_174', 'wizard', 'flash2', 'scilla', 'aspide', 'yoyo',
                  'rapper', 'phobos_1', 'upv-9596', 'nl_1b', 'tanzen', 'paperone', 'grezbot2', 'pirla', 'sgnaus',
                  'neo_sifr', 'pippo97', 'pognant', 'gundam', 'pippo99', 'argon', 'abyss', 'andrea97', 'slead',
                  'triangol', 'beast', 'paolo', 'deluxe', 'rambo3', 'twins', 'runner', 'vocus', 'd_ray', 'hal9002',
                  'revenge3', 'arale', 'passion', 'warrior3', 'deluxe_2', 'china', 'lead1', 'robbie', '!', 'duke',
                  'apache95', 'robivinf', 'cube', 'buffy', 'apache', 'wassilij', 'tm', 'rambo', 'lbr1', 'flash4',
                  'sassy', 'sentry', 'lucifer', 'hamp1', 'piperita', 'macchia', 'flash', 'jazz', 'pippo98', 'leavy',
                  'heavnew2', 'heavnew3', 'goldrake', 'robocop2', 'heavnew', 'spot', 'uht', 'superfly', 'ninus6',
                  'lukather', 'diagonal', 'isaac', 'et_4', 'paranoid', 't1001', 'navaho', 'hamp2', 'mimo6new', 'fdig',
                  'traker1', 'et_5', 'godel', 'gevbass', 'mister2', 'mrcc', 'paolo77', 'maxheav', 'mimo13', 'baeos',
                  'mister3b', 'blade3', 'max10', 'cspotrun', 'cw', 'mister3', 'jagger', 'risc', 'vannina', 'gazi',
                  'robocop3', 'ken', 'marco', 'ninus99', 'bry_bry', 'ninus75', 'bronx-00', 'nexus_1', 'biro', 'cortez',
                  '8bismark', 'phobos_2', 'surrende', 'briscolo', 'yuri', 'matrox', 'ai2', 'warrior2', 'static',
                  'ninus17', 'ai1', 'wolfgang', 'fastfood', 'banzel', 'secro', 'nexus_2_2', 'halman', 'ice', 'rattolo',
                  't-rex', 'kenii', 'spartaco', 'uhm', 'mikezhar', 'pikachu', 'second3', 'clover', 'deluxe_4',
                  'mflash2', 'elija', 'hitnrun', 'skizzo', 'lazy', 'torneo', 'chase', 'cri95', 'corner4', 'trio',
                  'tmii', 'jager', 'sp', 'ola', 'stush-1', 'qibo', 'vikingo', 'me-110c', 'perizoom', 'robocop',
                  'courage', 'baubau', 'r_daneel', 'the_dam', 'dia', 'thunder', 'titania', 'losendos', 'robot2_2',
                  'titania2', 'diablo2', 'bachopin', 'f1', 'genesis', 'corner3b', 'dorsai', 'corner3', 'dima10',
                  'polluce', 'robot1_2', 'raid2', 'raid3', 'blade8', '(c)', 'herpes', 'diablo3', 'corner1d', 'dave_2',
                  'sara_6', 'klr2', 'flash3', 'intrcptr', 'ld', 'rocco', 'nexus_2', 'animal', 'shadow', 'daitan3',
                  'golem2', 'adversar', 'miaomiao', 'tricky', 'boom', 'warrior4', 'mcenrobo', 'cantor', 'gira',
                  'kamikaze', 'plump', 'bishop', 'spinner', 'sdc2', 'hal9000', 'lbr', 'robot1', 'lebbra', 'valevan',
                  'pippo96b', 'paolo101', 'crob1', 'chobin', 'themicro', 'pippo95', 'camillo', 'nl_2a', 'pippo96a',
                  'superv', 's-seven', 'aleph', 'zulu', 'crm', 'horse2', 'cassius', 'tracker', 'horse', 'iching',
                  'stighy98', 'gunnyb29', 'pippo', 'carla', 'golem', 'boss', 'castore', 'pippo94a', 'pavido', 'pippo92',
                  'diablo', 'lethal', 'mutation', 'ciccio', 'nl_2b', 'patcioca', 'tronco', 'fb3', 'morituro', 'brain',
                  'penta', 'belva', 'killer3', 'p68', 'biro3', 'ap_5', 'seeker', 'horse3', 'di', 'blob', 'venom', 'p69',
                  'pippo00', 'colera', 'geriba', 'johnny', 'erica', 'emanuela', 'r_cyborg', '01', 'paccu', 'cooper2',
                  'risk', 'tifo', 'selvaggio', 'bouncer', 'torchio', 'topgun', 'robot2', 'grunt', 'ap_2', 'frame',
                  'robocop_2', 'nemesi', 'deluxe_5', 'polipo', 'cooper1', 'stinger', 'randwall', 'flyby', 'xhatch',
                  'archer', 'reflex', 'tatank_3', 'p', 'funky', 'ematico', 'giali1', 'pippo00a', 'boxer', 'catfish3',
                  'ortica', 'anglek2', 'food5', 'andrea96', 'mg_three', 'target', 'etf_kid', 'ap_1', 'peribolo',
                  'natas', 'gpo2', 'grezbot', 'quack', 'poor', 'fscan', 'maverick', 'raid', 'seekem', 'd47', 'peste',
                  'hider2', 'circlek1', 'carlo96', 'biro2', 'genius_j', 'killer', 'ninja', 'jet', 'schwan', 'scan',
                  'marvin', 'didimo', 'shark4', 'ninja2', 'puyopuyo', 'hell', 'hak3', 'assassin2', 'jack', 'eva01',
                  'shark3', 'rabbit10', 'rungun', 'pacio', 'fermo', 'hunter3', 'vaiolo', 'gunner', 'toppa', 'didimo2',
                  'scanlock', 'murdoc', 'friendly', 'b115e2', 'sdix3', 'saxy', 'geltrude', 'jolly', 'marika', 'mohawk',
                  'spider', 'watchdog', 'crazy', 'thorin', 'heavens', 'pippo94b', 'micro', 'ogre', 'mini', 'casimiro',
                  'cruiser', 'duck', 'eva00', 'assassin', 'carlo', 'xdraw2', 'twedlede', 'premana', 'twedledm',
                  'foursquare', 'stalker', 'trial4', 'hitman', 'instict', 'tron', 'andrea', 'yal', 'samurai', 'dima9',
                  'heavens2', 'adam', 'antru', 'ogre3', 'zorro', 'pioppo', 'ninja3', 'uanino', 'ccyber', 'pipp1', 'sel',
                  'anticlock', 'ogre2', 'quikshot', 'gsmr2', 'dancer', 'gossamer', 'pest', '666', 'tiger', 'mg_one',
                  'sshooter', 'pingpong', 'scanner3', 'star', 'hunter', 'scanner', 'chaser', 'rob1', 'h-k', 'swirl',
                  'mg_two', 'counter2', 'rapest', 'et_3', 't1000', 'jason100', 'york', 'xecutner', 'avoider', 'casual',
                  'squirrel', 'killer2', 'kami', 'mut', 'et_2', 'fred', 'doppia_g', 'phantom', 'agressor', 'whirlwind',
                  'tabori-1', 'tabori-2', 'circle', 'gunnyboy', 'pzkmin', 'traker2', 'ap_4', 'blindschl', 'counter',
                  'nord2', 'zioalfa', 'dicin', 'sniper', 'pzk', 'pardoner', 'ridicol', 'opfer', 'maniac', 't-rex2',
                  'et_1', 'xenon', 'silly', 'blindschl2', 'danimal', 'rook', 'nord', 'dirtyh', 'cornerkl', 'random',
                  'hac_atak', 'dumbname', 'beaver', 'mirobot', 'b4', 'aswhup', 'sidewalk', 'randguard', 'mike3',
                  'pippo15b', 'circles15', 'babadook', 'pantagruel', 'lluke', 'salippo', 'g13-14', 'wall-e_v',
                  'hal9015', 'the_old', 'pippo15a', 'gargantua', 'antman', 'flash9', 'frank15', 'tux', 'gerty4',
                  'tyrion', 'dlrn', 'bttf', 'corbu15', 'misdemeano', 'thor', 'puppet', 'mcfly', 'jedi13', 'ironman_15',
                  'music', 'coppi15ma1', 'colour', 'linabo15', 'one', 'hulk', 'coppi15mc1', 'coppi15md1', 'mies15',
                  'coppi15ma2']