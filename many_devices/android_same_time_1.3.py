#%%

from adbutils import adb
import re
import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor

deviceId_d = {"A-002": "98899a334c42393842", "A-003": "ce07171774ef249f0c7e", "A-004": "4a32454738573398", "A-005": "R28M302NRLP", "A-006": "R28M217V37V", "A-007": "R28M224QE1R", "A-008": "98899538534d30395a", "A-009": "TWGDU16712000560", "A-010": "GSLDU16712001946", "A-012": "FFKDU17324008871", "A-013": "8f75d00b", "A-014": "SJE5T17311006237", "A-015": "8BN0217615005367", "A-016": "68UDU17B25001167", "A-017": "UYT0217A17007198", "A-018": "A5R4C17A10006833", "A-019": "RKKDU17C07001790", "A-020": "CLB0218326000191", "A-021": "VBJ4C18505013951", "A-022": "6EJ7N18602004216", "A-023": "66J5T18A04011733", "A-024": "LKN5T18A28000905", "A-025": "S2D0218A14001419", "A-026": "GPG4C19109006895", "A-027": "5ENDU19220008005", "A-028": "Q5S5T19319001858", "A-029": "MQS7N19330000429", "A-031": "17b7fcdd", "A-032": "3cab06ec", "A-033": "bb23b469", "A-034": "c9ede2de", "A-035": "3413ca56", "A-036": "IRMV79MV99999999", "A-037": "dc40d636", "A-038": "7127dad7", "A-039": "325ff27c", "A-040": "ab61dc25", "A-042": "d4aadf60", "A-043": "fc173d15", "A-044": "176980fa", "A-045": "9TJNTCUGA6RWTKKZ", "A-047": "928QAEVM22CVR", "A-048": "8739ca59", "A-049": "fdc9ae6", "A-050": "e87bc4e8", "A-051": "6763ac89", "A-053": "e5eedc51", "A-055": "S8AQSCN7FUNNU4LN", "A-052": "9ea5c212", "A-056": "UO799SY56TJV8HS8", "A-057": "TWJV5DL7FAQ4DIAQ", "A-058": "a8e94bd8", "A-059": "2aadb0a7", "A-060": "b97e66eb", "A-054": "75WS6TOZFUNRS4K7", "A-061": "PKT4C20416000911", "A-062": "4bca9a0b", "A-063": "HKL4BUAQ", "A-065": "e819cce6", "A-068": "712QACS6A9T5R", "A-069": "851QFDSE22CNY", "A-070": "882QADTESZP33", "A-071": "NX508J", "A-072": "8e56e898", "A-064": "HPV105R3", "A-073": "1e9c5005", "A-074": "d15fa94a", "A-075": "363f83db", "A-076": "1b79d561", "A-077": "f88f888b", "A-079": "8f8fe6e7", "A-082": "4310a633", "A-083": "f40f43a9", "A-081": "e9c684af", "A-084": "8ae817fb", "A-085": "cb5c511a", "A-088": "6059c075", "A-089": "fcc7b75d", "A-090": "CLB7N18927006324", "A-092": "38d42fc1", "A-093": "NJ5SV8S4TGYSAYHU", "A-091": "d94897ce", "A-094": "VBJDU18C21004669", "A-095": "4527a64", "A-097": "d20fc41d", "A-101": "RPG0218C04000164", "A-102": "CUYDU19523010244", "A-100": "cf65dcc4", "A-103": "ERLDU19611000738", "A-104": "OBU4B6L7UWAUNBZ5", "A-105": "SKRGJ7WSQWZP59AY", "A-106": "HKP3A6TK", "A-107": "325da15f", "A-108": "971QAEUSYEAJY", "A-109": "9f116227", "A-110": "0123456789ABCDEF", "A-112": "f6e0a42b", "A-113": "98de436d", "A-114": "7HX0219912018795", "A-115": "JTK5T19911030787", "A-116": "5eff3022", "A-117": "d6497dee", "A-118": "28c820dc", "A-119": "f4adfe27", "A-120": "294cd7c4", "A-147": "S8M6R20612006563", "A-156": "AWMCUT1208018025", "A-177": "AKRSVB1715005843", "A-148": "000002b72c2d43ce", "A-173": "D12113910208", "A-149": "H4K5T20B26002336", "A-163": "30521250220057M", "A-158": "181QGEYB225PD", "A-166": "caa3dc4e", "A-160": "9652026725001EX", "A-161": "e2346635", "A-152": "68789dec", "A-153": "75UWQSCMT8UKZTOF", "A-169": "RXD0221624011395", "A-165": "9548702557001JR", "A-151": "0123456789ABCDEF", "A-164": "eb9eaa6b", "A-159": "d10fcb41", "A-168": "c61d6f69", "A-157": "9652519021002S4", "A-170": "CAP7CMPFR8TSHUOR", "A-171": "3142504081000KQ", "A-150": "1207a7cb", "A-175": "181QGEZ52222X", "A-178": "CP031212211976", "A-180": "d19bf8b4", "A-143": "081668f60404", "A-141": "danjvsemukr4ssea", "A-142": "0209b8b70403", "A-172": "t4wogmifem55jvto", "A-174": "57c55e9a", "A-179": "0123456789ABCDEF", "A-146": "823aa6f6", "A-144": "b84bf414", "A-140": "pvnbt4q8t8w4offi", "A-139": "MDEBB20621205941", "A-145": "R5CR10PFAGH", "A-162": "eb30857", "A-155": "320813796545", "A-133": "XPC0220413003662", "A-138": "0123456789ABCDEF", "A-137": "NAB0220414052732", "A-136": "Z81QAEWNM6TAF", "A-135": "41e5d75b", "A-154": "2b94d3b5383f7ece", "A-134": "0123456789ABCDEF", "A-132": "QKXUT20519008497", "A-131": "KSACP19911C01541", "A-130": "e8003b59", "A-128": "0123456789ABCDEF", "A-123": "E3LBB20313219581", "A-125": "5b2b8563", "A-121": "efb7a711", "A-126": "b3538589", "A-122": "b787f745", "A-124": "8UJDU19B20007775", "A-235": "RFCT810MM6T", "A-240": "RFCMA01NV4L", "A-197": "R28M31LFCHP", "A-233": "10AD6Q2X33001AU", "A-223": "ZY22GDCN2F", "A-224": "ZY22GMNKF6", "A-226": "2f20296", "A-238": "Q5S5T19313002347", "A-234": "381QYFD2227KW", "A-187": "S8OJVWZPC6ZHEIL7", "A-239": "MQS7N19402000374", "A-230": "320235652205", "A-222": "10AD1B0SH400129", "A-218": "Y5XSWCGIQW9LYL6L", "A-193": "YDDYLFHAGQ4DWGCA", "A-190": "172QHEZG225LR", "A-188": "34127415650010C", "A-185": "4a45a976", "A-182": "A3SRBB1A16017600", "A-220": "BLT0222C02003436", "A-192": "a1b1357c", "A-129": "d906466a", "A-186": "fff093b0", "A-183": "SED0221903005000", "A-212": "4d6299c", "A-204": "ZY22DRNPVF", "A-208": "151a4b3c", "A-216": "10AC841GT60023P", "A-209": "AB9E022208000162", "A-214": "10HC6103EE0027G", "A-195": "1567410593001JO", "A-196": "V900S1112400796", "A-210": "UDU0221708005242", "A-200": "31586603510002T", "A-201": "341326954700137", "A-202": "abef13d0", "A-205": "2cbd53f3", "A-243": "ADFDU19C03011699", "A-244": "28cd9ed5", "A-242": "d6833c08", "A-241": "340c532b", "A-250": "99031FFAZ009WG", "A-245": "d479031c", "A-249": "1f6971ea", "A-247": "32c0a8f1", "A-258": "5ee0de88", "A-257": "20cc4eb", "A-253": "ac25eae9", "A-252": "ZY224763Z6", "A-254": "a66ae422", "A-255": "NNHA69CQGEE6Z9NZ", "A-256": "f9d8ccb2", "A-259": "3HX7N16B23004697", "A-260": "40e3e84f", "A-261": "6102bc3c", "A-262": "14e3448f", "A-264": "aeb3f0fe", "A-263": "10ADBM0HZ5001XF", "A-266": "O7MJAAM79PTGNVRG", "A-268": "10CE1P0F2S000E5", "A-283": "481QFFEA229XH", "A-286": "2NP0224424003082", "A-282": "DU8TT84HE6AYSGSC", "A-285": "S2AIOC455518AKM", "A-284": "2UCUT24111017703", "A-281": "32020DLH2000AA", "A-269": "10ADBR1C87001RP", "A-274": "ANASUT3C22003546", "A-184": "AQHMBB1813001012"}
deviceName_d = {"98899a334c42393842": "A-002", "ce07171774ef249f0c7e": "A-003", "4a32454738573398": "A-004", "R28M302NRLP": "A-005", "R28M217V37V": "A-006", "R28M224QE1R": "A-007", "98899538534d30395a": "A-008", "TWGDU16712000560": "A-009", "GSLDU16712001946": "A-010", "FFKDU17324008871": "A-012", "8f75d00b": "A-013", "SJE5T17311006237": "A-014", "8BN0217615005367": "A-015", "68UDU17B25001167": "A-016", "UYT0217A17007198": "A-017", "A5R4C17A10006833": "A-018", "RKKDU17C07001790": "A-019", "CLB0218326000191": "A-020", "VBJ4C18505013951": "A-021", "6EJ7N18602004216": "A-022", "66J5T18A04011733": "A-023", "LKN5T18A28000905": "A-024", "S2D0218A14001419": "A-025", "GPG4C19109006895": "A-026", "5ENDU19220008005": "A-027", "Q5S5T19319001858": "A-028", "MQS7N19330000429": "A-029", "17b7fcdd": "A-031", "3cab06ec": "A-032", "bb23b469": "A-033", "c9ede2de": "A-034", "3413ca56": "A-035", "IRMV79MV99999999": "A-036", "dc40d636": "A-037", "7127dad7": "A-038", "325ff27c": "A-039", "ab61dc25": "A-040", "d4aadf60": "A-042", "fc173d15": "A-043", "176980fa": "A-044", "9TJNTCUGA6RWTKKZ": "A-045", "928QAEVM22CVR": "A-047", "8739ca59": "A-048", "fdc9ae6": "A-049", "e87bc4e8": "A-050", "6763ac89": "A-051", "e5eedc51": "A-053", "S8AQSCN7FUNNU4LN": "A-055", "9ea5c212": "A-052", "UO799SY56TJV8HS8": "A-056", "TWJV5DL7FAQ4DIAQ": "A-057", "a8e94bd8": "A-058", "2aadb0a7": "A-059", "b97e66eb": "A-060", "75WS6TOZFUNRS4K7": "A-054", "PKT4C20416000911": "A-061", "4bca9a0b": "A-062", "HKL4BUAQ": "A-063", "e819cce6": "A-065", "712QACS6A9T5R": "A-068", "851QFDSE22CNY": "A-069", "882QADTESZP33": "A-070", "NX508J": "A-071", "8e56e898": "A-072", "HPV105R3": "A-064", "1e9c5005": "A-073", "d15fa94a": "A-074", "363f83db": "A-075", "1b79d561": "A-076", "f88f888b": "A-077", "8f8fe6e7": "A-079", "4310a633": "A-082", "f40f43a9": "A-083", "e9c684af": "A-081", "8ae817fb": "A-084", "cb5c511a": "A-085", "6059c075": "A-088", "fcc7b75d": "A-089", "CLB7N18927006324": "A-090", "38d42fc1": "A-092", "NJ5SV8S4TGYSAYHU": "A-093", "d94897ce": "A-091", "VBJDU18C21004669": "A-094", "4527a64": "A-095", "d20fc41d": "A-097", "RPG0218C04000164": "A-101", "CUYDU19523010244": "A-102", "cf65dcc4": "A-100", "ERLDU19611000738": "A-103", "OBU4B6L7UWAUNBZ5": "A-104", "SKRGJ7WSQWZP59AY": "A-105", "HKP3A6TK": "A-106", "325da15f": "A-107", "971QAEUSYEAJY": "A-108", "9f116227": "A-109", "0123456789ABCDEF": "A-128", "f6e0a42b": "A-112", "98de436d": "A-113", "7HX0219912018795": "A-114", "JTK5T19911030787": "A-115", "5eff3022": "A-116", "d6497dee": "A-117", "28c820dc": "A-118", "f4adfe27": "A-119", "294cd7c4": "A-120", "S8M6R20612006563": "A-147", "AWMCUT1208018025": "A-156", "AKRSVB1715005843": "A-177", "000002b72c2d43ce": "A-148", "D12113910208": "A-173", "H4K5T20B26002336": "A-149", "30521250220057M": "A-163", "181QGEYB225PD": "A-158", "caa3dc4e": "A-166", "9652026725001EX": "A-160", "e2346635": "A-161", "68789dec": "A-152", "75UWQSCMT8UKZTOF": "A-153", "RXD0221624011395": "A-169", "9548702557001JR": "A-165", "eb9eaa6b": "A-164", "d10fcb41": "A-159", "c61d6f69": "A-168", "9652519021002S4": "A-157", "CAP7CMPFR8TSHUOR": "A-170", "3142504081000KQ": "A-171", "1207a7cb": "A-150", "181QGEZ52222X": "A-175", "CP031212211976": "A-178", "d19bf8b4": "A-180", "081668f60404": "A-143", "danjvsemukr4ssea": "A-141", "0209b8b70403": "A-142", "t4wogmifem55jvto": "A-172", "57c55e9a": "A-174", "823aa6f6": "A-146", "b84bf414": "A-144", "pvnbt4q8t8w4offi": "A-140", "MDEBB20621205941": "A-139", "R5CR10PFAGH": "A-145", "eb30857": "A-162", "320813796545": "A-155", "XPC0220413003662": "A-133", "NAB0220414052732": "A-137", "Z81QAEWNM6TAF": "A-136", "41e5d75b": "A-135", "2b94d3b5383f7ece": "A-154", "QKXUT20519008497": "A-132", "KSACP19911C01541": "A-131", "e8003b59": "A-130", "E3LBB20313219581": "A-123", "5b2b8563": "A-125", "efb7a711": "A-121", "b3538589": "A-126", "b787f745": "A-122", "8UJDU19B20007775": "A-124", "RFCT810MM6T": "A-235", "RFCMA01NV4L": "A-240", "R28M31LFCHP": "A-197", "10AD6Q2X33001AU": "A-233", "ZY22GDCN2F": "A-223", "ZY22GMNKF6": "A-224", "2f20296": "A-226", "Q5S5T19313002347": "A-238", "381QYFD2227KW": "A-234", "S8OJVWZPC6ZHEIL7": "A-187", "MQS7N19402000374": "A-239", "320235652205": "A-230", "10AD1B0SH400129": "A-222", "Y5XSWCGIQW9LYL6L": "A-218", "YDDYLFHAGQ4DWGCA": "A-193", "172QHEZG225LR": "A-190", "34127415650010C": "A-188", "4a45a976": "A-185", "A3SRBB1A16017600": "A-182", "BLT0222C02003436": "A-220", "a1b1357c": "A-192", "d906466a": "A-129", "fff093b0": "A-186", "SED0221903005000": "A-183", "4d6299c": "A-212", "ZY22DRNPVF": "A-204", "151a4b3c": "A-208", "10AC841GT60023P": "A-216", "AB9E022208000162": "A-209", "10HC6103EE0027G": "A-214", "1567410593001JO": "A-195", "V900S1112400796": "A-196", "UDU0221708005242": "A-210", "31586603510002T": "A-200", "341326954700137": "A-201", "abef13d0": "A-202", "2cbd53f3": "A-205", "ADFDU19C03011699": "A-243", "28cd9ed5": "A-244", "d6833c08": "A-242", "340c532b": "A-241", "99031FFAZ009WG": "A-250", "d479031c": "A-245", "1f6971ea": "A-249", "32c0a8f1": "A-247", "5ee0de88": "A-258", "20cc4eb": "A-257", "ac25eae9": "A-253", "ZY224763Z6": "A-252", "a66ae422": "A-254", "NNHA69CQGEE6Z9NZ": "A-255", "f9d8ccb2": "A-256", "3HX7N16B23004697": "A-259", "40e3e84f": "A-260", "6102bc3c": "A-261", "14e3448f": "A-262", "aeb3f0fe": "A-264", "10ADBM0HZ5001XF": "A-263", "O7MJAAM79PTGNVRG": "A-266", "10CE1P0F2S000E5": "A-268", "481QFFEA229XH": "A-283", "2NP0224424003082": "A-286", "DU8TT84HE6AYSGSC": "A-282", "S2AIOC455518AKM": "A-285", "2UCUT24111017703": "A-284", "32020DLH2000AA": "A-281", "10ADBR1C87001RP": "A-269", "ANASUT3C22003546": "A-274", "AQHMBB1813001012": "A-184"}
class DeviceAndroid():
    def __init__(self,deviceId) -> None:
        self.deviceId = deviceId
        self.adb_d = adb.device(deviceId)
        self.max_x = int(re.split(r' +',re.search(r'max +[0-9]+',re.findall(r' +0035 +: value +[0-9]+, +min +[0-9]+, +max +[0-9]+',self.adb_d.shell("getevent -p"))[-1]).group(0))[1])
        self.max_y = int(re.split(r' +',re.search(r'max +[0-9]+',re.findall(r' +0036 +: value +[0-9]+, +min +[0-9]+, +max +[0-9]+',self.adb_d.shell("getevent -p"))[-1]).group(0))[1])
        self.direction = self.adb_d.rotation()

    def check_direction(self):
        self.direction = self.adb_d.rotation()
        return self.direction
    
    def out_relative_position_x(self,x_p):
        x_i = int(x_p,16)
        return x_i/self.max_x

    def out_relative_position_y(self,y_p):
        y_i = int(y_p,16)
        return y_i/self.max_y
    
    def refrash(self):
        self.max_x = int(re.split(r' +',re.search(r'max +[0-9]+',re.findall(r' +0035 +: value +[0-9]+, +min +[0-9]+, +max +[0-9]+',self.adb_d.shell("getevent -p"))[-1]).group(0))[1])
        self.max_y = int(re.split(r' +',re.search(r'max +[0-9]+',re.findall(r' +0036 +: value +[0-9]+, +min +[0-9]+, +max +[0-9]+',self.adb_d.shell("getevent -p"))[-1]).group(0))[1])

    def tap(self,positionx,positiony,direction):
        if direction==0:
            print("tap",positionx,positiony)
            self.adb_d.click(positionx,positiony)
        elif direction==1:
            print("tap",positiony,1-positionx)
            self.adb_d.click(positiony,1-positionx)
        elif direction==3:
            print("tap",1-positiony,positionx)
            self.adb_d.click(1-positiony,positionx)


    def swipe(self,position_x,position_y,position_x1,position_y1,direction):
        if direction == 0:
            print("swipe",position_x,position_y,position_x1,position_y1,0.3)
            self.adb_d.swipe(position_x,position_y,position_x1,position_y1,0.3)
        elif direction == 1:
            print("swipe",position_y,1-position_x,position_y1,1-position_x1,0.3)
            self.adb_d.swipe(position_y,1-position_x,position_y1,1-position_x1,0.3)
        elif direction == 3:
            print("swipe",1-position_y,position_x,1-position_y1,position_x1,0.3)
            self.adb_d.swipe(1-position_y,position_x,1-position_y1,position_x1,0.3)

def do_tap(devices_set,position,direction):
    for shouji in devices_set:
        threading.Thread(target=shouji.tap,args=(position[0][0],position[0][1],direction)).start()

def do_swipe(devices_set,position,direction):
    for shouji in devices_set:
        threading.Thread(target=shouji.swipe,args=(position[0][0],position[0][1],position[1][0],position[1][1],direction)).start()

def out_pos(f,position,device_list,que):
    while True:
        if device_list != adb.list():
            f.close()
            que.put("stop")
            return 0
        line = f.readline()
        info_serch = re.search(r'ABS_MT_POSITION_X +[0-9a-f]{8}|ABS_MT_POSITION_Y +[0-9a-f]{8}|BTN_TOUCH +UP',line)
        if info_serch != None:
            search_result = re.split(r' +',info_serch.group(0))
            if search_result[0] == "ABS_MT_POSITION_X":
                temp_x = MainDevice.out_relative_position_x(search_result[1])
                if len(position) < 2:
                    position.append([temp_x,0])
                else:
                    position[1][0] = temp_x
            elif search_result[0] == "ABS_MT_POSITION_Y":
                temp_y = MainDevice.out_relative_position_y(search_result[1])
                if len(position) == 0:
                    position.append([temp_x,temp_y])
                else:
                    position[-1][1] = temp_y
            elif search_result[0] == "BTN_TOUCH":
                if search_result[1] == "UP":
                    if len(position) == 1:
                        direction = MainDevice.check_direction()
                        que.put(("tap",position,direction))
                    elif len(position) == 2:
                        if abs(position[0][0]-position[1][0])>distance or abs(position[0][1]-position[1][1])>distance:
                            direction = MainDevice.check_direction()
                            que.put(("swipe",position,direction))
                        else:
                            direction = MainDevice.check_direction()
                            que.put(("tap",position,direction))
                    position = []

def do_it(devices_set,que):
    threadPool = ThreadPoolExecutor(max_workers=len(devices_set),thread_name_prefix="test_")
    while True:
        vir = que.get()
        if vir[0] == "tap":
            for shouji in devices_set:
                threadPool.submit(shouji.tap, vir[1][0][0],vir[1][0][1],vir[2])
        elif vir[0] == "swipe":
            for shouji in devices_set:
                threadPool.submit(shouji.swipe, vir[1][0][0],vir[1][0][1],vir[1][1][0],vir[1][1][1],vir[2])

        elif vir == "stop":
            threadPool.shutdown(wait=True)
            return 0




que = Queue(maxsize=0)

while True:
    device_list = adb.list()
    devices = adb.device_list()
    MainDeviceName = input("主控设备名:")
    if MainDeviceName == "":
        MainDeviceName = deviceName_d[devices[0].serial]
    print("主控设备名称：",MainDeviceName,"\n脚本初始化,请稍候")
    MainDevice = DeviceAndroid(deviceId_d[MainDeviceName])
    print(MainDevice.max_x,MainDevice.max_y)
    devices_set = set()
    for dev in adb.device_list():
        if dev.serial != deviceId_d[MainDeviceName]:
            d = DeviceAndroid(dev.serial)
            print(deviceName_d[d.deviceId],d.adb_d.window_size())
            devices_set.add(d)
    print("检测到{n}台设备".format(n=len(devices_set)))
    stream = MainDevice.adb_d.shell("getevent -l | grep -E 'ABS_MT_POSITION|BTN_TOUCH'", stream=True)
    running = 0
    distance = 0.05
    threadPool = ThreadPoolExecutor(max_workers=len(devices_set),thread_name_prefix="test_")
    with stream:
        f = stream.conn.makefile()
        position = []
        posx_temp = 0
        print("初始化完成，可以开始操作了！")
        t1 = threading.Thread(target=out_pos,args=(f,position,device_list,que))
        t1.start()
        # t2 = threading.Thread(target=do_it,args=(devices_set,que))
        # t2.start()
        do_it(devices_set,que)





























# while True:
#     device_list = adb.list()
#     devices = adb.device_list()
#     MainDeviceName = input("主控设备名:")
#     if MainDeviceName == "":
#         MainDeviceName = deviceName_d[devices[0].serial]
#     print("主控设备名称：",MainDeviceName,"\n脚本初始化,请稍候")
#     MainDevice = DeviceAndroid(deviceId_d[MainDeviceName])
#     temp = MainDevice.adb_d.shell("getevent -p")
#     print(MainDevice.max_x,MainDevice.max_y)
#     devices_set = set()
#     for dev in adb.device_list():
#         if dev.serial != deviceId_d[MainDeviceName]:
#             d = DeviceAndroid(dev.serial)
#             print(deviceName_d[d.deviceId],d.adb_d.window_size())
#             devices_set.add(d)
#     print("检测到{n}台设备".format(n=len(devices_set)))
#     stream = MainDevice.adb_d.shell("getevent -l | grep -E 'ABS_MT_POSITION|BTN_TOUCH'", stream=True)
#     running = 0
#     distance = 0.05
#     threadPool = ThreadPoolExecutor(max_workers=len(devices_set),thread_name_prefix="test_")
#     with stream:
#         f = stream.conn.makefile()
#         position = []
#         posx_temp = 0
#         print("初始化完成，可以开始操作了！")
#         while True:
#             if device_list != adb.list():
#                 f.close()
#                 break
#             line = f.readline()
#             info_serch = re.search(r'ABS_MT_POSITION_X +[0-9a-f]{8}|ABS_MT_POSITION_Y +[0-9a-f]{8}|BTN_TOUCH +UP',line)
#             if info_serch != None:
#                 search_result = re.split(r' +',info_serch.group(0))
#                 if search_result[0] == "ABS_MT_POSITION_X":
#                     temp_x = MainDevice.out_relative_position_x(search_result[1])
#                     if len(position) < 2:
#                         position.append([temp_x,0])
#                     else:
#                         position[1][0] = temp_x

#                 elif search_result[0] == "ABS_MT_POSITION_Y":
#                     temp_y = MainDevice.out_relative_position_y(search_result[1])
#                     if len(position) == 0:
#                         position.append([temp_x,temp_y])
#                     else:
#                         position[-1][1] = temp_y


#                 elif search_result[0] == "BTN_TOUCH":
#                     if search_result[1] == "UP":
#                         if len(position) == 1:
#                             # threading.Thread(target=do_tap,args=(devices_set,position,MainDevice.check_direction())).start()
#                             que.put[(devices_set,position,MainDevice.check_direction())]
#                         elif len(position) == 2:
#                             if abs(position[0][0]-position[1][0])>distance or abs(position[0][1]-position[1][1])>distance:
#                                 # threading.Thread(target=do_swipe,args=(devices_set,position,MainDevice.check_direction())).start()
#                                 que.put[(devices_set,position,MainDevice.check_direction())]
#                             else:
#                                 # threading.Thread(target=do_tap,args=(devices_set,position,MainDevice.check_direction())).start()
#                                 que.put[(devices_set,position,MainDevice.check_direction())]
#                         position=[]






