import uiautomator2 as u2
import tempfile
import vobject
import os

class vCard(u2.Device):

    def phone2vcard(self, phones:list):
        """手机转vCard
        """
        def vcard(phone:str):
            VCARD='''BEGIN:VCARD
VERSION:2.1
N;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:;%s;;;
TEL;VOICE:%s
END:VCARD
''' % (phone, phone)
            return VCARD
        f = ''
        for phone in phones:
            f += vcard(phone)
        return f
    
    def vcard2phones(self, vcard_path:str):
        """vCard文件转手机号
        """
        vcard = ''
        with open(vcard_path, 'r') as f:
            vcard = f.read()
        vc = vobject.readComponents(vcard)
        return [c.fn.value for c in vobject.readComponents(vcard)]

    def vcard_to_host(self, app_name:str='com.android.contacts', filepath:str='/storage/self/primary/00001.vcf'):
        """vCard文件拷贝到主机
        """
        self.app_stop(app_name)
        self.app_start(app_name)
        self(resourceId="com.android.contacts:id/overflow_menu_contacts").click()
        self.sleep(0.3)
        self.xpath('//android.widget.ListView/android.widget.LinearLayout[3]/android.widget.RelativeLayout[1]').click()
        self(resourceId="android:id/title", text="导出到存储设备").click()
        self(resourceId="android:id/button1").click()
        self(resourceId="android:id/text1", text="Telegram\n5688817166").click()
        self(resourceId="android:id/button1").click()
        dst = os.path.join(tempfile.gettempdir(), os.path.split(filepath)[1])
        self.sleep(2)
        self.pull(filepath, dst)
        self.del_vcard(filepath)
        return dst
    
    def vcard_to_device(self, vcardtext:str='', filepath:str='/storage/self/primary/00001.vcf'):
        """vCard文件拷贝入设备
        """
        tmpfd, tmpfn = tempfile.mkstemp('.vcf')
        with open(tmpfn, 'a') as f:
            f.write(vcardtext)
        self.push(tmpfn, filepath)

    def import_vcard(self, filepath:str='file:///storage/self/primary/00001.vcf'):
        """导入vCard
        """
        cmd = 'am start -t "text/x-vcard" -d "' + filepath + '" -a android.intent.action.VIEW com.android.contacts'
        self.shell(cmd)
        self(text='确定').click()
    
    def del_vcard(self, filepath:str='/storage/self/primary/00001.vcf'):
        """删除vCard文件
        """
        self.shell('rm -f ' + filepath)

    def clear_contacts(self):
        """清除联系人
        """
        cmd = 'pm clear com.android.providers.contacts'
        self.shell(cmd)
    
    def reset_telegram(self, app_name:str='org.telegram.messenger.web'):
        self.app_stop(app_name)
        self.app_start(app_name)
    
    def detect_phones(self, phones:list):
        """检测手机号码
        """
        self.clear_contacts()
        vfstr = self.phone2vcard(phones)
        self.vcard_to_device(vfstr)
        self.import_vcard()
        self.reset_telegram()
        self.sleep(6)
        device_vcard_path = '/storage/sdcard1/00001.vcf'
        return self.vcard2phones(self.vcard_to_host(filepath=device_vcard_path))

    
if __name__ == '__main__':
    # err_phones = ['84344181593', '84929297780']
    d = vCard('KWG5T16328005311')
    # # d = vCard('DRB5T18719014355')
    # d.clear_contacts()
    # # users = ['84922309089', '84922009077', '84562997613', '84854141245', '84352079053']
    # vfstr = d.phone2vcard(err_phones)
    # d.vcard_to_device(vfstr)
    # d.import_vcard()
    # d.reset_telegram()

    # debug pull vcard
    # d.pull_vcard()
    