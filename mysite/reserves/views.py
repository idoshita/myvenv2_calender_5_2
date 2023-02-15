from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Store,Staff,Booking,MaxNum,DefaultValue
from datetime import datetime,date,timedelta,time
from django.db.models import Q
from django.utils.timezone import localtime,make_aware
from reserves.forms import BookingForm,MaxNumForm,DefaultValueForm,MaxNumeForm
from django.views.decorators.http import require_POST

#make_awareとは、「2019/10/28 13:07」のような時間を時間として認識する。naive timeは、逆に、「2019/10/28 13:07」のような時間を時間でなく文字として認識する。


class StoreView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:#is_authenticartedとは、ログインしていたらTrueを返す。もしuserがログインしていたら、
            # staff_data = Staff.objects.filter(store=store_data).select_related("user")
            start_date = date.today()
            # weekday = start_date.weekday()
            # if weekday != 6:#もし今日の日付が日曜日でなければ、
            #     start_date = start_date - timedelta(days=weekday + 1)#今週の日曜日をstart_dateに設定する。
            return redirect("reserves_mypage",start_date.year,start_date.month,start_date.day)#URLに開始日時の情報を渡している。
        store_data = Store.objects.all()#すべてのadminに登録されているstoreデータを取得する。

        return render(request, "reserves/store.html",{
            "store_data":store_data,
        })


class StaffView(View):
    def get(self, request, *args, **kwargs):
        store_data = get_object_or_404(Store, id=self.kwargs["pk"])#もしstoreデータがない場合には、404が返される。idは、URLに記載してあるPKから取得する。
        staff_data = Staff.objects.filter(store=store_data).select_related("user")#select_relatedを実行することで、userへのSQL実行回数を減らすことができる。つまり、パソコン内にキャッシュを残すことができるようになり、staffデータとstoreデータで紐づけられてるuserデータの読み込みがスムーズになる。

        return render(request, "reserves/staff.html",{
            "store_data":store_data,
            "staff_data":staff_data,
        })


class CalendarView(View):
    def get(self, request, *args, **kwargs):
        staff_data1 = Staff.objects.filter(id=self.kwargs["pk"])#[0]#.select_related("user").select_related("store")[0]#Staffデータの中から、URLのPKデータとIDが一致する人をstaff_dataとする。
        staff_data = staff_data1[0]
        #python内では、filterは、リスト形式の[キー:値]の形式で出力される。
        #[0]などで、リストの番号を指定することで、リストの0番目のデータが値の形で取り出す事が出来る。
        #[0]を使用しない場合には、リストを関数でstaff_data = staff_data1[0]で値の形で取り出す事により、値の形で取り出すことができる。
        #.select_related("user").select_related("store")で、userデータとstoreデータのキャッシュを残すことで、データ読み込み処理を早める。この処理は、calendar.htmlで呼び出す際に必要になる。
        today = date.today()
        year = self.kwargs.get("year")#URLからyearを取得する。
        month = self.kwargs.get("month")#URLからmonthを取得する。
        day = self.kwargs.get("day")#URLからdayを取得する。
        if year and month and day:#もし日付が指定されている場合、つまりURLにyear,month,dayが存在する場合、
            start_date = date(year=year, month=month, day=day)#URLの日時をstart_dateにする。
        else:
            start_date = today
        days = [start_date + timedelta(days=day) for day in range(7)]#start_dateから7日間をdaysとして設定し、daysを利用して後々カレンダーに設定する。
        start_day = days[0]#上記で定めたfor文の中の、start_dateから7日間が、daysのリスト形式になっているため、daysのリスト形式の0番目の値をstart_dayとする。
        end_day = days[-1]#上記で定めたfor文の中の、start_dateから7日間が、daysのリスト形式になっているため、daysのリスト形式の-1番目(一番最後の日)の値をend_dayとする。


        start_time = make_aware(datetime.combine(start_day,time(hour=10,minute=0,second=0)))#開始時間を作成している。
        end_time = make_aware(datetime.combine(end_day,time(hour=20,minute=0,second=0)))#終了時間を作成している。
        booking_data = Booking.objects.filter(staff=staff_data).exclude(Q(start__gt=end_time)|Q(end__lt=start_time))

        kokok = DefaultValue.objects.all()
        defae = list(kokok.values())
        defaem = defae[-1]
        kokoo = [opopo for oioio, opopo in defaem.items()]
        defa = kokoo[-1]


        if booking_data:
            # for booking in booking_data:
            #     local_time = localtime(booking.start)#localtimeで現地時間で取得する。booking.startで、Bookingデータの中のstartを引っ張って、local_time関数に格納する。
                # booking_date = local_time.date()#上記のlocal_timeを、date()メソッドで、2022-11-12のような日付型に変更している。
                # booking_hour = local_time.hour#上記のlocal_timeの時間をbooking_hour関数に変更している。

            calendar = {}#空のディクショナリをcalendarという名前で作る。
            for hour in range(10,21):#10~21の数字をhourという関数で繰り返す。
                row = {}#空のディクショナリをrowという名前で作る。
                for day in days:#上記で定めたdaysのリストをdayという関数で繰り返す。
                    row[day] = defa#10~21の行を、start_day～end_dayまで列を繰り返す。
                calendar[hour] = row#二次元配列を利用している。10~21を繰り返したものを、daysの7日間繰り返す処理で、二次元配列を完成させている。



                for houre, schedules in calendar.items():
                    for datetimer, book in schedules.items():

                        datebook = make_aware(datetime.combine(datetimer,time(hour=houre)))
                        renum = Booking.objects.filter(staff=staff_data,start=datebook)
                        childnum = sum([i.childnum for i in renum])
                        adlutnum = sum([i.adlutnum for i in renum])
                        g = childnum + adlutnum




                        munum = MaxNum.objects.filter(starts=datebook).values_list('maxnum', flat=True)
                        for munumb in munum:



                            if (houre in calendar) and (datetimer in calendar[houre]) and (munumb-g <= 0):#calendarの中に、時間と日付が存在している場合、
                                calendar[houre][datetimer] = False #calendarの二次元配列の該当する箇所をFalseにすることで予約を設定している。calendarリスト(二次元配列になっているリスト)の中の、行が[booking_hour]番目のデータと、列が[booking_date]番目のデータをFalseにしている。
                            elif (houre in calendar) and (datetimer in calendar[houre]) and (0 != munumb-g):#calendarの中に、時間と日付が存在している場合、
                                calendar[houre][datetimer] = munumb-g #calendarの二次元配列の該当する箇所をFalseにすることで予約を設定している。calendarリスト(二次元配列になっているリスト)の中の、行が[booking_hour]番目のデータと、列が[booking_date]番目のデータをFalseにしている。

            return render(request, "reserves/calendar.html",{
                "staff_data":staff_data,
                "calendar":calendar,
                "days":days,
                "start_day":start_day,
                "end_day":end_day,
                "before":days[0] - timedelta(days=7),#beforeとは、timedeltaメソッドを使って、daysの0番目の7日前を表示する。
                "next":days[-1] + timedelta(days=1),#beforeとは、timedeltaメソッドを使って、daysの0番目の7日前を表示する。
                "today":today,
            })



        else:

            calendar = {}#空のディクショナリをcalendarという名前で作る。
            for hour in range(10,21):#10~21の数字をhourという関数で繰り返す。
                row = {}#空のディクショナリをrowという名前で作る。
                for day in days:#上記で定めたdaysのリストをdayという関数で繰り返す。
                    row[day] = defa#10~21の行を、start_day～end_dayまで列を繰り返す。
                calendar[hour] = row#二次元配列を利用している。10~21を繰り返したものを、daysの7日間繰り返す処理で、二次元配列を完成させている。

            return render(request, "reserves/calendar.html",{
                "staff_data":staff_data,
                "calendar":calendar,
                "days":days,
                "start_day":start_day,
                "end_day":end_day,
                "before":days[0] - timedelta(days=7),#beforeとは、timedeltaメソッドを使って、daysの0番目の7日前を表示する。
                "next":days[-1] + timedelta(days=1),#beforeとは、timedeltaメソッドを使って、daysの0番目の7日前を表示する。
                "today":today,
            })




class BookingView(View):
    def get(self, request, *args, **kwargs):
        staff_data = Staff.objects.filter(id=self.kwargs["pk"]).select_related("user").select_related("store")[0]
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        day = self.kwargs.get("day")
        hour = self.kwargs.get("hour")
        form = BookingForm(request.POST or None)
        return render(request,"reserves/booking.html",{
            "staff_data":staff_data,
            "year":year,
            "month":month,
            "day":day,
            "hour":hour,
            "form":form
        })

    def post(self, request, *args, **kwargs):
        staff_data = get_object_or_404(Staff, id=self.kwargs["pk"])
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        day = self.kwargs.get("day")
        hour = self.kwargs.get("hour")
        start_time =make_aware(datetime(year=year,month=month,day=day,hour=hour))#kwargsで取得できる時間から、ローカル時間で開始時間を作成する。
        end_time =make_aware(datetime(year=year,month=month,day=day,hour=hour + 1))#終了時間は、開始時間の1時間後に設定する。
        booking_data = Booking.objects.filter(staff=staff_data,start=start_time).count()#予約時間を、スタッフデータとスタートタイムでフィルターして取得する。つまり、Bookingデータの中でstaffがstaff_dataと一致して、startがstart_timeと一致するものをbooking_dataとして格納する。
        form = BookingForm(request.POST or None)
        munum = MaxNum.objects.filter(starts=start_time)

        kokok = DefaultValue.objects.all()
        defae = list(kokok.values())
        defaem = defae[-1]
        kokoo = [opopo for oioio, opopo in defaem.items()]
        defa = kokoo[-1]

        if munum and ((munum - booking_data) == 0):
            form.add_error(None,"既に予約が入ってしまいました。別の時間をお試しください。")

        else:
            if form.is_valid():
                #<input type="submit">を利用して送信ボタンを作成した場合には、formの未入力箇所があると、Djangoがエラーを警告してくれるが、
                #<a href>や<div>を利用して送信ボタンを作成した場合には、Djangoがエラーを返してくれないため、form.is_valid()で自分でエラー内容を作成する必要がある。
                booking = Booking()#models.pyのBookingクラスのデータをbookingとする。
                booking.staff = staff_data
                booking.start = start_time
                booking.end = end_time
                booking.first_name = form.cleaned_data["first_name"]
                booking.last_name = form.cleaned_data["last_name"]
                booking.tel = form.cleaned_data["tel"]
                booking.save()

                if munum:
                    return redirect("reserves_thanks")
                else:
                    mnunmer = MaxNum()
                    mnunmer.starts = start_time
                    mnunmer.ends = end_time
                    mnunmer.maxnum = defa
                    mnunmer.save()
                    return redirect("reserves_thanks")



        return render(request, "reserves/booking.html",{
            "staff_data":staff_data,
            "year":year,
            "month":month,
            "day":day,
            "hour":hour,
            "form":form,#formのバリデーションに失敗した場合には、予約画面に遷移します。
        })


class ThanksView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "reserves/thanks.html")


class MypageView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        staff_data = Staff.objects.filter(id=request.user.id).select_related("user").select_related("store")[0]
        year = self.kwargs.get("year")#URLからyearを取得する。
        month = self.kwargs.get("month")#URLからmonthを取得する。
        day = self.kwargs.get("day")#URLからdayを取得する。
        start_date = date(year=year, month=month, day=day)#URLの日時をstart_dateにする。

        days = [start_date + timedelta(days=day) for day in range(7)]#start_dateから7日間をdaysとして設定し、daysを利用して後々カレンダーに設定する。
        start_day = days[0]#上記で定めたfor文の中の、start_dateから7日間が、daysのリスト形式になっているため、daysのリスト形式の0番目の値をstart_dayとする。
        end_day = days[-1]#上記で定めたfor文の中の、start_dateから7日間が、daysのリスト形式になっているため、daysのリスト形式の-1番目(一番最後の日)の値をend_dayとする。
        start_time = make_aware(datetime.combine(start_day,time(hour=10,minute=0,second=0)))
        end_time = make_aware(datetime.combine(end_day,time(hour=20,minute=0,second=0)))
        booking_data = Booking.objects.filter(staff=staff_data).exclude(Q(start__gt=end_time)|Q(end__lt=start_time))

        kokok = DefaultValue.objects.all()
        defae = list(kokok.values())
        defaem = defae[-1]
        kokoo = [opopo for oioio, opopo in defaem.items()]
        defa = kokoo[-1]

        calendar = {}#空のディクショナリをcalendarという名前で作る。
        for hour in range(10,21):#10~21の数字をhourという関数で繰り返す。
            row = {}#空のディクショナリをrowという名前で作る。
            for dayn in days:#上記で定めたdaysのリストをdayという関数で繰り返す。
                row[dayn] = ""#10~21の行を、start_day～end_dayまで列を繰り返す。
            calendar[hour] = row#二次元配列を利用している。10~21を繰り返したものを、daysの7日間繰り返す処理で、二次元配列を完成させている。

            for houre, schedules in calendar.items():
                for datetimer, book in schedules.items():

                    datebook = make_aware(datetime.combine(datetimer,time(hour=houre)))
                    renum = Booking.objects.filter(staff=staff_data,start=datebook)
                    childnum = sum([i.childnum for i in renum])
                    adlutnum = sum([i.adlutnum for i in renum])
                    g = childnum + adlutnum

                    munum = MaxNum.objects.filter(starts=datebook).values_list('maxnum', flat=True)
                    for munumb in munum:

                        if (houre in calendar) and (datetimer in calendar[houre]) and munumb:#calendarの中に、時間と日付が存在している場合、
                            calendar[houre][datetimer] = f"{munumb-g}/{munumb}" #calendarの二次元配列の該当する箇所をFalseにすることで予約を設定している。calendarリスト(二次元配列になっているリスト)の中の、行が[booking_hour]番目のデータと、列が[booking_date]番目のデータをFalseにしている。
                        elif (houre in calendar) and (datetimer in calendar[houre]) and (munumb<=0):#calendarの中に、時間と日付が存在している場合、
                            calendar[houre][datetimer] = f"休" #calendarの二次元配列の該当する箇所をFalseにすることで予約を設定している。calendarリスト(二次元配列になっているリスト)の中の、行が[booking_hour]番目のデータと、列が[booking_date]番目のデータをFalseにしている。
                        else:#calendarの中に、時間と日付が存在している場合、
                            calendar[houre][datetimer] = f"{defa}/{defa}" #calendarの二次元配列の該当する箇所をFalseにすることで予約を設定している。calendarリスト(二次元配列になっているリスト)の中の、行が[booking_hour]番目のデータと、列が[booking_date]番目のデータをFalseにしている。



        return render(request, "reserves/mypage.html",{
            "booking_data":booking_data,
            "staff_data":staff_data,
            "defa":defa,
            "calendar":calendar,
            "days":days,
            "start_day":start_day,
            "end_day":end_day,
            "before":days[0] - timedelta(days=7),#beforeとは、timedeltaメソッドを使って、daysの0番目の7日前を表示する。
            "next":days[-1] + timedelta(days=1),#beforeとは、timedeltaメソッドを使って、daysの0番目の7日前を表示する。
            "year":year,
            "month":month,
            "day":day,
        })




@require_POST#ボタンが押された時のみ動作する。
def HolidayAll(request,year,month,day):
    staff_data = Staff.objects.get(id=request.user.id)
    start_date = date(year=year,month=month,day=day)




    t = make_aware(datetime.combine(start_date,time(hour=10,minute=0,second=0)))
    dt = make_aware(datetime.combine(start_date,time(hour=11,minute=0,second=0)))


    dt1 = make_aware(datetime.combine(start_date,time(hour=12,minute=0,second=0)))

    dt2 = make_aware(datetime.combine(start_date,time(hour=13,minute=0,second=0)))

    dt3 = make_aware(datetime.combine(start_date,time(hour=14,minute=0,second=0)))

    dt4 = make_aware(datetime.combine(start_date,time(hour=15,minute=0,second=0)))

    dt5 = make_aware(datetime.combine(start_date,time(hour=16,minute=0,second=0)))

    dt6 = make_aware(datetime.combine(start_date,time(hour=17,minute=0,second=0)))

    dt7 = make_aware(datetime.combine(start_date,time(hour=18,minute=0,second=0)))

    dt8 = make_aware(datetime.combine(start_date,time(hour=19,minute=0,second=0)))

    dt9 = make_aware(datetime.combine(start_date,time(hour=20,minute=0,second=0)))

    dt10 = make_aware(datetime.combine(start_date,time(hour=21,minute=0,second=0)))




    booking = MaxNum(maxnum=0, starts=t,ends=dt)
    booking.save()

    booking1 = MaxNum(maxnum=0, starts=dt,ends=dt1)
    booking1.save()

    booking2 = MaxNum(maxnum=0, starts=dt1,ends=dt2)
    booking2.save()

    booking3 = MaxNum(maxnum=0, starts=dt2,ends=dt3)
    booking3.save()

    booking4 = MaxNum(maxnum=0, starts=dt3,ends=dt4)
    booking4.save()

    booking5 = MaxNum(maxnum=0, starts=dt4,ends=dt5)
    booking5.save()

    booking6 = MaxNum(maxnum=0, starts=dt5,ends=dt6)
    booking6.save()

    booking7 = MaxNum(maxnum=0, starts=dt6,ends=dt7)
    booking7.save()

    booking8 = MaxNum(maxnum=0, starts=dt7,ends=dt8)
    booking8.save()

    booking9 = MaxNum(maxnum=0, starts=dt8,ends=dt9)
    booking9.save()

    booking10 = MaxNum(maxnum=0, starts=dt9,ends=dt10)
    booking10.save()


    today_data = date.today()
    today_data1 = date.today() + timedelta(days=1)
    today_data2 = date.today() + timedelta(days=2)
    today_data3 = date.today() + timedelta(days=3)
    today_data4 = date.today() + timedelta(days=4)
    today_data5 = date.today() + timedelta(days=5)
    today_data6 = date.today() + timedelta(days=6)
    today_data7 = date.today() + timedelta(days=7)


    if start_date==today_data or start_date==today_data1 or start_date==today_data2 or start_date==today_data3 or start_date==today_data4 or start_date==today_data5 or start_date==today_data6:
        start_date = date.today()
    else:
        start_date = today_data7

    return redirect("reserves_mypage",year=start_date.year,month=start_date.month,day=start_date.day)



@require_POST#ボタンが押された時のみ動作する。
def Holiday(self,year,month,day,hour):

    start_time = make_aware(datetime(year=year,month=month,day=day,hour=hour))#開始時間を作成している。
    end_time = make_aware(datetime(year=year,month=month,day=day,hour=hour +1 ))#終了時間を作成している。

    MaxNum.objects.create(#create関数でBookingオブジェクトに登録が可能となる。
        maxnum = 0,
        starts = start_time,
        ends = end_time
    )

    start_date = date(year=year,month=month,day=day)


    today_data = date.today()
    today_data1 = date.today() + timedelta(days=1)
    today_data2 = date.today() + timedelta(days=2)
    today_data3 = date.today() + timedelta(days=3)
    today_data4 = date.today() + timedelta(days=4)
    today_data5 = date.today() + timedelta(days=5)
    today_data6 = date.today() + timedelta(days=6)
    today_data7 = date.today() + timedelta(days=7)


    if start_date==today_data or start_date==today_data1 or start_date==today_data2 or start_date==today_data3 or start_date==today_data4 or start_date==today_data5 or start_date==today_data6:
        start_date = date.today()
    else:
        start_date = today_data7

    return redirect("reserves_mypage",year=start_date.year,month=start_date.month,day=start_date.day)



@require_POST#ボタンが押された時のみ動作する。
def Delete(request,year,month,day,hour):
    staff_data = Staff.objects.get(id=request.user.id)
    start_time = make_aware(datetime(year=year,month=month,day=day,hour=hour))
    booking_data = Booking.objects.filter(start=start_time)

    booking_data.delete()#Bookingオブジェクトを削除している。

    start_date = date(year=year,month=month,day=day)

    today_data = date.today()
    today_data1 = date.today() + timedelta(days=1)
    today_data2 = date.today() + timedelta(days=2)
    today_data3 = date.today() + timedelta(days=3)
    today_data4 = date.today() + timedelta(days=4)
    today_data5 = date.today() + timedelta(days=5)
    today_data6 = date.today() + timedelta(days=6)
    today_data7 = date.today() + timedelta(days=7)


    if start_date==today_data or start_date==today_data1 or start_date==today_data2 or start_date==today_data3 or start_date==today_data4 or start_date==today_data5 or start_date==today_data6:
        start_date = date.today()
    else:
        start_date = today_data7



    return redirect("reserves_mypage",year=start_date.year,month=start_date.month,day=start_date.day)





class NumChange(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        # print(request.GET)
        staff_data = Staff.objects.filter(id=request.user.id).select_related("user").select_related("store")[0]
        forme = MaxNumForm(request.POST or None)
        formes = DefaultValueForm(request.POST or None)
        formee = MaxNumeForm(request.POST or None)
        today = date.today()
        year = self.kwargs.get("year")#URLからyearを取得する。
        month = self.kwargs.get("month")#URLからmonthを取得する。
        day = self.kwargs.get("day")#URLからdayを取得する。
        if year and month and day:#もし日付が指定されている場合、つまりURLにyear,month,dayが存在する場合、
            start_date = date(year=year, month=month, day=day)#URLの日時をstart_dateにする。
        else:
            start_date = today
        days = [start_date + timedelta(days=day) for day in range(7)]#start_dateから7日間をdaysとして設定し、daysを利用して後々カレンダーに設定する。
        start_day = days[0]#上記で定めたfor文の中の、start_dateから7日間が、daysのリスト形式になっているため、daysのリスト形式の0番目の値をstart_dayとする。
        end_day = days[-1]#上記で定めたfor文の中の、start_dateから7日間が、daysのリスト形式になっているため、daysのリスト形式の-1番目(一番最後の日)の値をend_dayとする。


        kokok = DefaultValue.objects.all()
        defae = list(kokok.values())
        defaem = defae[-1]
        kokoo = [opopo for oioio, opopo in defaem.items()]
        defa = kokoo[-1]



        calendar = {}#空のディクショナリをcalendarという名前で作る。
        for hour in range(10,21):#10~21の数字をhourという関数で繰り返す。
            row = {}#空のディクショナリをrowという名前で作る。
            for day in days:#上記で定めたdaysのリストをdayという関数で繰り返す。
                row[day] = defa#10~21の行を、start_day～end_dayまで列を繰り返す。
            calendar[hour] = row#二次元配列を利用している。10~21を繰り返したものを、daysの7日間繰り返す処理で、二次元配列を完成させている。

            # print(calendar)

            for houre, schedules in calendar.items():
                for datetimer, book in schedules.items():

                    datebook = make_aware(datetime.combine(datetimer,time(hour=houre)))
                    renum = Booking.objects.filter(staff=staff_data,start=datebook)
                    childnum = sum([i.childnum for i in renum])
                    adlutnum = sum([i.adlutnum for i in renum])
                    g = childnum + adlutnum




                    munum = MaxNum.objects.filter(starts=datebook).values_list('maxnum', flat=True)
                    for munumb in munum:



                        if (houre in calendar) and (datetimer in calendar[houre]) and munumb:#calendarの中に、時間と日付が存在している場合、
                            calendar[houre][datetimer] = f"{munumb-g}/{munumb}" #calendarの二次元配列の該当する箇所をFalseにすることで予約を設定している。calendarリスト(二次元配列になっているリスト)の中の、行が[booking_hour]番目のデータと、列が[booking_date]番目のデータをFalseにしている。
                        elif (houre in calendar) and (datetimer in calendar[houre]) and (munumb<=0):#calendarの中に、時間と日付が存在している場合、
                            calendar[houre][datetimer] = f"休み設定中" #calendarの二次元配列の該当する箇所をFalseにすることで予約を設定している。calendarリスト(二次元配列になっているリスト)の中の、行が[booking_hour]番目のデータと、列が[booking_date]番目のデータをFalseにしている。
                        else:#calendarの中に、時間と日付が存在している場合、
                            calendar[houre][datetimer] = f"{defa}/{defa}" #calendarの二次元配列の該当する箇所をFalseにすることで予約を設定している。calendarリスト(二次元配列になっているリスト)の中の、行が[booking_hour]番目のデータと、列が[booking_date]番目のデータをFalseにしている。



        return render(request, "reserves/numchange.html",{
            "staff_data":staff_data,
            "calendar":calendar,
            "defa":defa,
            "forme":forme,
            "formes":formes,
            "formee":formee,
            "days":days,
            "start_day":start_day,
            "end_day":end_day,
            "before":days[0] - timedelta(days=7),#beforeとは、timedeltaメソッドを使って、daysの0番目の7日前を表示する。
            "next":days[-1] + timedelta(days=1),#beforeとは、timedeltaメソッドを使って、daysの0番目の7日前を表示する。
            "today":today,
        })


    def post(self, request, *args, **kwargs):

        forme = MaxNumForm(request.POST or None)
        formes = DefaultValueForm(request.POST or None)
        formee = MaxNumeForm(request.POST or None)
        # print(request.POST["maxnum"])
        # print(request.POST["btn_num"])
        # print(request.POST["startse_date"])
        # print(request.POST["starts_hour"])
        if formee.is_valid():
            hoge = request.POST["startse_date"].replace('年', '-')
            hoge1 = hoge.replace('月', '-')
            hoge2 = hoge1.replace('日', '')
            i = hoge2 + " " + "10:00:00"
            t = datetime.strptime(i,"%Y-%m-%d %H:%M:%S")
            m = hoge2 + " " + "11:00:00"
            dt = datetime.strptime(m,"%Y-%m-%d %H:%M:%S")

            m1 = hoge2 + " " + "12:00:00"
            dt1 = datetime.strptime(m1,"%Y-%m-%d %H:%M:%S")

            m2 = hoge2 + " " + "13:00:00"
            dt2 = datetime.strptime(m2,"%Y-%m-%d %H:%M:%S")

            m3 = hoge2 + " " + "14:00:00"
            dt3 = datetime.strptime(m3,"%Y-%m-%d %H:%M:%S")

            m4 = hoge2 + " " + "15:00:00"
            dt4 = datetime.strptime(m4,"%Y-%m-%d %H:%M:%S")

            m5 = hoge2 + " " + "16:00:00"
            dt5 = datetime.strptime(m5,"%Y-%m-%d %H:%M:%S")

            m6 = hoge2 + " " + "17:00:00"
            dt6 = datetime.strptime(m6,"%Y-%m-%d %H:%M:%S")

            m7 = hoge2 + " " + "18:00:00"
            dt7 = datetime.strptime(m7,"%Y-%m-%d %H:%M:%S")

            m8 = hoge2 + " " + "19:00:00"
            dt8 = datetime.strptime(m8,"%Y-%m-%d %H:%M:%S")

            m9 = hoge2 + " " + "20:00:00"
            dt9 = datetime.strptime(m9,"%Y-%m-%d %H:%M:%S")

            m10 = hoge2 + " " + "21:00:00"
            dt10 = datetime.strptime(m10,"%Y-%m-%d %H:%M:%S")

            booking = MaxNum()#models.pyのBookingクラスのデータをbookingとする。
            booking.maxnum = request.POST["maxnum"]
            booking.starts = t
            booking.ends = dt
            booking.save()

            booking1 = MaxNum()
            booking1.maxnum = request.POST["maxnum"]
            booking1.starts = dt
            booking1.ends = dt1
            booking1.save()

            booking2 = MaxNum()
            booking2.maxnum = request.POST["maxnum"]
            booking2.starts = dt1
            booking2.ends = dt2
            booking2.save()

            booking3 = MaxNum()
            booking3.maxnum = request.POST["maxnum"]
            booking3.starts = dt2
            booking3.ends = dt3
            booking3.save()

            booking4 = MaxNum()
            booking4.maxnum = request.POST["maxnum"]
            booking4.starts = dt3
            booking4.ends = dt4
            booking4.save()

            booking5 = MaxNum()
            booking5.maxnum = request.POST["maxnum"]
            booking5.starts = dt4
            booking5.ends = dt5
            booking5.save()

            booking6 = MaxNum()
            booking6.maxnum = request.POST["maxnum"]
            booking6.starts = dt5
            booking6.ends = dt6
            booking6.save()

            booking7 = MaxNum()
            booking7.maxnum = request.POST["maxnum"]
            booking7.starts = dt6
            booking7.ends = dt7
            booking7.save()

            booking8 = MaxNum()
            booking8.maxnum = request.POST["maxnum"]
            booking8.starts = dt7
            booking8.ends = dt8
            booking8.save()

            booking9 = MaxNum()
            booking9.maxnum = request.POST["maxnum"]
            booking9.starts = dt8
            booking9.ends = dt9
            booking9.save()

            booking10 = MaxNum()
            booking10.maxnum = request.POST["maxnum"]
            booking10.starts = dt9
            booking10.ends = dt10
            booking10.save()
            return redirect("reserves_numchange")


        if forme.is_valid():

            hoge = request.POST["starts_date"].replace('年', '-')
            hoge1 = hoge.replace('月', '-')
            hoge2 = hoge1.replace('日', '')
            i = hoge2 + " " + request.POST["starts_hour"] + ":00:00"
            t = datetime.strptime(i,"%Y-%m-%d %H:%M:%S")
            j = int(request.POST["starts_hour"])+1
            m = hoge2 + " " + str(j) + ":00:00"
            dt = datetime.strptime(m,"%Y-%m-%d %H:%M:%S")

            booking = MaxNum()#models.pyのBookingクラスのデータをbookingとする。
            booking.maxnum = request.POST["maxnum"]
            booking.starts = t
            booking.ends = dt
            booking.save()
            return redirect("reserves_numchange")


        if formes.is_valid():
            bookinger = DefaultValue()#models.pyのBookingクラスのデータをbookingとする。
            bookinger.defaultvalue = request.POST["defaultvalue"]
            bookinger.save()
            return redirect("reserves_numchange")




        staff_data = Staff.objects.filter(id=request.user.id).select_related("user").select_related("store")[0]
        today = date.today()
        year = self.kwargs.get("year")#URLからyearを取得する。
        month = self.kwargs.get("month")#URLからmonthを取得する。
        day = self.kwargs.get("day")#URLからdayを取得する。
        if year and month and day:#もし日付が指定されている場合、つまりURLにyear,month,dayが存在する場合、
            start_date = date(year=year, month=month, day=day)#URLの日時をstart_dateにする。
        else:
            start_date = today
        days = [start_date + timedelta(days=day) for day in range(7)]#start_dateから7日間をdaysとして設定し、daysを利用して後々カレンダーに設定する。
        start_day = days[0]#上記で定めたfor文の中の、start_dateから7日間が、daysのリスト形式になっているため、daysのリスト形式の0番目の値をstart_dayとする。
        end_day = days[-1]#上記で定めたfor文の中の、start_dateから7日間が、daysのリスト形式になっているため、daysのリスト形式の-1番目(一番最後の日)の値をend_dayとする。


        kokok = DefaultValue.objects.all()
        defae = list(kokok.values())
        defaem = defae[-1]
        kokoo = [opopo for oioio, opopo in defaem.items()]
        defa = kokoo[-1]



        calendar = {}#空のディクショナリをcalendarという名前で作る。
        for hour in range(10,21):#10~21の数字をhourという関数で繰り返す。
            row = {}#空のディクショナリをrowという名前で作る。
            for day in days:#上記で定めたdaysのリストをdayという関数で繰り返す。
                row[day] = defa#10~21の行を、start_day～end_dayまで列を繰り返す。
            calendar[hour] = row#二次元配列を利用している。10~21を繰り返したものを、daysの7日間繰り返す処理で、二次元配列を完成させている。

            for houre, schedules in calendar.items():
                for datetimer, book in schedules.items():

                    datebook = make_aware(datetime.combine(datetimer,time(hour=houre)))
                    renum = Booking.objects.filter(staff=staff_data,start=datebook)
                    childnum = sum([i.childnum for i in renum])
                    adlutnum = sum([i.adlutnum for i in renum])
                    g = childnum + adlutnum




                    munum = MaxNum.objects.filter(starts=datebook).values_list('maxnum', flat=True)
                    for munumb in munum:



                        if (houre in calendar) and (datetimer in calendar[houre]) and munumb:#calendarの中に、時間と日付が存在している場合、
                            calendar[houre][datetimer] = f"{munumb-g}/{munumb}" #calendarの二次元配列の該当する箇所をFalseにすることで予約を設定している。calendarリスト(二次元配列になっているリスト)の中の、行が[booking_hour]番目のデータと、列が[booking_date]番目のデータをFalseにしている。
                        elif (houre in calendar) and (datetimer in calendar[houre]) and (munumb<=0):#calendarの中に、時間と日付が存在している場合、
                            calendar[houre][datetimer] = f"休み設定中" #calendarの二次元配列の該当する箇所をFalseにすることで予約を設定している。calendarリスト(二次元配列になっているリスト)の中の、行が[booking_hour]番目のデータと、列が[booking_date]番目のデータをFalseにしている。
                        else:#calendarの中に、時間と日付が存在している場合、
                            calendar[houre][datetimer] = f"{defa}/{defa}" #calendarの二次元配列の該当する箇所をFalseにすることで予約を設定している。calendarリスト(二次元配列になっているリスト)の中の、行が[booking_hour]番目のデータと、列が[booking_date]番目のデータをFalseにしている。



        return render(request, "reserves/numchange.html",{
            "staff_data":staff_data,
            "forme":forme,
            "formes":formes,
            "formee":formee,
            "calendar":calendar,
            "days":days,
            "start_day":start_day,
            "end_day":end_day,
            "before":days[0] - timedelta(days=7),#beforeとは、timedeltaメソッドを使って、daysの0番目の7日前を表示する。
            "next":days[-1] + timedelta(days=1),#beforeとは、timedeltaメソッドを使って、daysの0番目の7日前を表示する。
            "today":today,
        })
    



class Toreserves(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        year = self.kwargs.get("year")#URLからyearを取得する。
        month = self.kwargs.get("month")#URLからmonthを取得する。
        day = self.kwargs.get("day")#URLからdayを取得する。
        hour = self.kwargs.get("hour")#URLからdayを取得する。
        start_date = datetime(year=year, month=month, day=day, hour=hour)
        booking_data = Booking.objects.filter(start=start_date)
        book_child = sum([book.childnum for book in booking_data])
        book_adlut = sum([book.adlutnum for book in booking_data])
        book_num = book_child + book_adlut

        return render(request, "reserves/toreserves.html",{
            "booking_data":booking_data,
            "start_date":start_date,
            "book_num":book_num,
            "book_child":book_child,
            "book_adlut":book_adlut,

        })
