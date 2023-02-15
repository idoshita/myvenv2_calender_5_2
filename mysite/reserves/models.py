from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
from accounts.models import CustomUser
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

class Store(models.Model):#店舗のモデルを作成する。
    name = models.CharField("店舗",max_length=100)
    address = models.CharField("住所",max_length=100,null=True,blank=True)
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$")
    tel = models.CharField("電話番号",validators = [phoneNumberRegex], max_length = 16, unique = True,null=True,blank=True)
    description = models.TextField("説明",default="",blank=True)
    image = models.ImageField(upload_to="images", verbose_name="イメージ画像",null=True,blank=True)

    def __str__(self):#管理画面に表示されるモデル内のデータ（レコード）を判別するための、名前（文字列）を定義することができます。つまり、adminにログインしてStoreを開いた時に、nameを表示してね。の設定。
        return self.name


class Staff(models.Model):
    user = models.OneToOneField(CustomUser, verbose_name="スタッフ", on_delete=models.CASCADE)#OneToOneFieldとは、引数のCustomUserモデルを利用し、CustomUserモデルに、Staffクラスで追加する項目を追加できるようにするメソッドである。StaffとCustomUserを合致させている。
    store = models.ForeignKey(Store, verbose_name="店舗", on_delete=models.CASCADE)#OneToOneFieldでCustomUserとStaffを紐づけ、ForeignKeyで店舗を設定しているので、CustomUserは、店舗（Store）の掛け持ちが出来なくなる。

    def __str__(self):
        return f"{self.store}:{self.user}"


class Booking(models.Model):
    staff = models.ForeignKey(Staff, verbose_name="スタッフ",on_delete=models.CASCADE)#on_delete=models.CASCADEとは、紐づくStaffモデルが削除された場合、それに紐づくBookingも一緒に削除する設定。
    first_name = models.CharField("姓",max_length=100,null=True,blank=True)
    last_name = models.CharField("名",max_length=100,null=True,blank=True)
    childnum = models.PositiveIntegerField("子供予約数",default=0,blank=True,validators=[MaxValueValidator(3)])
    adlutnum = models.PositiveIntegerField("大人予約数",default=1,blank=True,validators=[MaxValueValidator(3)])
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$")
    tel = models.CharField("電話番号",validators = [phoneNumberRegex], max_length = 16,null=True,blank=True)
    # remarks = models.TextField("備考",default="",blank=True)#備考は複数行を想定されるため、default=""と記述
    start = models.DateTimeField("開始時間",default=timezone.now)
    end = models.DateTimeField("終了時間",default=timezone.now)

    def __str__(self):
        start = timezone.localtime(self.start).strftime("%Y/%m/%d %H:%M") #localtimeを利用することでDjangoで設定したタイムゾーンの時間に変更される。
        end = timezone.localtime(self.end).strftime("%Y/%m/%d %H:%M")

        return f"{self.first_name}{self.last_name}{start}～{end}{self.staff}"#adminの管理画面で、予約した名前と予約した時間が表示される。


class MaxNum(models.Model):
    maxnum = models.PositiveIntegerField("予約最大数",blank=True)
    starts = models.DateTimeField("開始時間",default=timezone.now)
    ends = models.DateTimeField("終了時間",default=timezone.now)

    def __str__(self):
        starts = timezone.localtime(self.starts).strftime("%Y/%m/%d %H:%M") #localtimeを利用することでDjangoで設定したタイムゾーンの時間に変更される。
        ends = timezone.localtime(self.ends).strftime("%Y/%m/%d %H:%M")

        return f"{starts}～{ends}{self.maxnum}"#adminの管理画面で、予約した名前と予約した時間が表示される。


class DefaultValue(models.Model):
    defaultvalue = models.IntegerField("全日予約数",blank=True)

    def __str__(self):
        return f"{self.defaultvalue}"
