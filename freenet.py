# -*- coding: utf-8 -*-
import redis,sys,os
from telebot import TeleBot
from telebot import types
from multiprocessing import Process, freeze_support
from khayyam import JalaliDatetime
from time import time
db = redis.StrictRedis(host='localhost', port=6379, db=14)
token = "433762647:AAFnHoCjnYRS0Qey8qPItY-5Sl322Q07Jng"
bot = TeleBot(token,threaded=True)
boti_info = bot.get_me()
admins = [438573461,304933903]
reload(sys)
sys.setdefaultencoding('utf-8')
# Values
adv_photo = "./adv.jpg"
link_cmd = "/link"
internet_cmd = "/internet"
channel = "Fun_GramTel"
members_must = 15
members_must2 = 18
internet_choices = ["ایرانسل", "همراه اول", "رایتل"]
string = {
	"start" : ""سلام {} ، {} شما بخیر
شما هم میتوانید 25 گیگابایت اینترنت رایگان هدیه بگیرید!
.
برای دریافت هدیه خود، ابتدا بروی {} کلیک و سپس اوپراتور خود را انتخاب کنید :"",
	"status" : "📊 راهنما و وضعیت من 📊",
	"status_txt" : ""برای دریافت 25 گیگ اینترنت رایگان خود، بروی {} کلیک کنید و سپس پیام جدیدی که دریافت میکنید را برای {} نفر ارسال کنید

تاکنون {} نفر روی لینک شما کلیک کرده ..."",
	"join_channel" : """برای استفاده از این روبات حتما باید در کانال زیر عضو باشید
پس از عضویت در کانال زیر، به روبات بازگردید و /start را لمس کنید"",
   "members_must" : ""🌹 سلام دوست عزیز . شما برنده ی 25 گیگ اینترنت 3 ماهه شدید . 
برای دریافت این جایزه کافیست 3 نفر دیگر را در ربات دعوت کنید ."",
   "members_must2" : ""⚠️ دوست گرامی این ربات به علت تخلف مسدود شد و شما برای گرفتن اینترنت نامحدود 2 ماهه به ربات جدید مراجعه کنید @internet_zbot برای دعوت 
دوستان، روی {} کلیک کنید."",
	"link_txt" : ""سریع تو روبات زیر ثبت نام کن و جز مشترک هر اوپراتوری که هستی، 25 گیگ اینترنت سه ماهه هدیه بگیر!

Telegram.me/{}?start={}

فرصت محدوده، عجله کن  "",
	"internet_choose" : """لطفا اوپراتور سیمکارت خود را مشخص کنید :""",
	"ich_error" : """پاسخ شما صحیح نیست. پاسخ ارسالی شما باید با استفاده از صفحه کلید زیر باشد:""",
	"ich_send_num" : """لطفا اکنون شماره خود را جهت دریافت اینترنت ارسال کنید :""",
	"ich_submited" : ""شماره شما با موفقیت ثبت شد!

اکنون بروی {} کلیک کنید و سپس پیام جدیدی که دریافت میکنید را برای {} نفر فوروارد کنید.
سپس بسته اینترنت رایگان، برای سیمکارت شما فعال خواهد شد""
}
def timetostr(time) :
	day = 0
	hour = 0
	minute = 0
	sec = 0
	if time > (24 * 60 * 60) :
		day = int(time/(24 * 60 * 60))
		time = time - (day * 24 * 60 * 60)
	if time > (60 * 60) :
		hour = int(time / (60 * 60))
		time = time - (hour * 60 * 60)
	if time > (60) :
		minute = int(time / (60))
		time = time - (minute * 60)
	sec = int(time)
	stri = ''
	backwrited = False
	if day > 0 :
		stri += str(day) + ' روز '
		backwrited = True
	if hour > 0 :
		if backwrited :
			stri += "و "
		stri += str(hour) + ' ساعت '
		backwrited = True
	if minute > 0 :
		if backwrited :
			stri += "و "
		stri += str(minute) + ' دقیقه '
		backwrited = True
	if sec > 0	:
		if backwrited :
			stri += "و "
		stri += str(sec)+' ثانیه'
		backwrited = True
	return stri
def ug(user,key) :
	return db.hget("user:"+str(user),key)
def us(user,key,value) :
	return db.hset("user:"+str(user),key,value)
def ur(user,key) :
	return db.hdel("user:"+str(user),key)
def mainkb(user) :
	if ug(user, "geted_link") :
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		markup.row(string["status"])
		return markup
	else :
		return types.ReplyKeyboardRemove(selective = True)
# Get Stringed Data Of A User 
def inf(user,html=False) :
	if isinstance(user, int): 
		try :
			chat = bot.get_chat(user)
		except :
			return str(user)
	else :
		chat = user
	if chat.username :
		chat.username= "[@"+chat.username+"] "
	else :
		chat.username = ""
	return str(chat.first_name)+" "+chat.username+"("+str(chat.id)+')'
print(boti_info)
@bot.message_handler()
def main(m):
	def main_multi() :
		try :
			if not db.sismember("bot:users",m.from_user.id) :
				sub = None
				if m.text and m.text.startswith("/start ") :
					sub = m.text.replace("/start ","")
				if sub and db.sismember("bot:users",int(sub)) :
					sub = int(sub)
					db.sadd("user:"+str(sub)+":subs",m.from_user.id)
					try :
						bot.send_message(sub,'🚀 کاربر\n'+inf(m.from_user)+'\nبه عنوان زیر مجموعه شما وارد ربات شد.')
					except :
						pass
			w = ug(m.from_user.id,"waiting")
			if ug(m.from_user.id, "geted_link") :
				check = False
				try :
					check = bot.get_chat_member("@"+channel , m.from_user.id).status in ["creator", "administrator", "member"]
				except :
					pass
				if check == False :
					markup = types.InlineKeyboardMarkup()
					markup.row(types.InlineKeyboardButton(text="@"+channel,url="https://telegram.me/"+channel))
					bot.reply_to(m, string["join_channel"], reply_markup = markup)
					return
			if	m.text.startswith("/start") or not db.sismember("bot:users",m.from_user.id) :
				db.sadd("bot:users",m.from_user.id)
				bot.reply_to(m,string["start"].format(m.from_user.first_name, JalaliDatetime.now().strftime('%A'), internet_cmd),reply_markup = mainkb(m.from_user.id))
				us(m.from_user.id,"waiting","main")
			elif m.text == string["status"] :
				bot.reply_to(m, string["status_txt"].format(link_cmd, members_must, db.scard("user:"+str(m.from_user.id)+":subs")), reply_markup = mainkb(m.from_user.id))
			elif m.text == link_cmd :
				us(m.from_user.id, "geted_link", True)
				file = open(adv_photo, "rb")
				bot.send_photo(m.chat.id, file, string["link_txt"].format(boti_info.username, m.from_user.id), reply_markup = mainkb(m.from_user.id), reply_to_message_id = m.message_id)
				file.close()
			elif m.text == internet_cmd :
				markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
				markup.add(*internet_choices)
				bot.reply_to(m, string["internet_choose"], reply_markup = markup)
				us(m.from_user.id, "waiting", "ich")
			elif w == "ich" :
				if m.text in internet_choices :
					bot.reply_to(m, string["ich_send_num"], reply_markup = types.ReplyKeyboardRemove(selective = True))
					us(m.from_user.id, "waiting", "ich2")
				else :
					bot.reply_to(m, string["ich_error"], reply_markup = markup)
			elif w == "ich2" :
				bot.reply_to(m, string["ich_submited"].format(link_cmd, members_must), reply_markup = mainkb(m.from_user.id))
				us(m.from_user.id, "waiting", "main")
			elif m.from_user.id in admins :
				if m.text == "/stats"  :
					bot.reply_to(m,"💠 تعداد کاربران : "+str(db.scard("bot:users")))
				elif m.text.startswith("/bc ") :
					ntime = time()
					textt = m.text.replace("/bc ","")
					glist = db.smembers("bot:users")
					agcount = len(glist)
					suc = 0 
					fail = 0
					bot.reply_to(m,"شروع شد!")
					for gp in glist :
						try :
							bot.send_message(gp,textt)
							suc += 1
						except Exception as e :
							se = str(e)
							if "Bad Request: message to forward not found" in se :
								bot.reply_to(m,"🔸 پیام برای ارسال یافت نشد.")
								if suc != 0 :
									bot.reply_to(m,"✨ پیام به "+str(suc + fail)+" کاربر از "+str(agcount)+" کاربر ربات ارسال شد\n\n☑️ موفق : "+str(suc)+"\n\n🔘 ناموفق : "+str(fail))
									us(bid,m.from_user.id,"waiting","main")
								return
							elif "bot was blocked by the user" in se:
								inviter = ug(gp,"host")
								if inviter :
									bot.send_message(inviter,"😪 کاربر "+inf(int(gp))+" از لیست کاربران شما حذف شد .")
								db.srem("bot:users",gp)
							fail += 1
					bot.reply_to(m,"✨ پیام به "+str(suc + fail)+" کاربر از "+str(agcount)+" کاربر ربات ارسال شد\n\n☑️ موفق : "+str(suc)+"\n\n🔘 ناموفق : "+str(fail)+"\nزمان : "+timetostr(time() - ntime))
		except Exception as e :
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno,e)
	freeze_support()
	Process(target=main_multi).start()
bot.polling(none_stop=True)
