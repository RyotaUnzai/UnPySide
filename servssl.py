import datetime
import glob
import ipaddress
import os
import subprocess
import tkinter as tk
import uuid
from tkinter import messagebox

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import (Encoding,
                                                          NoEncryption,
                                                          PrivateFormat,
                                                          pkcs12)
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID

# from OpenSSL import crypto


Serial = ""
Password = ""


def isPem():
    pempath = "./" + "127.0.0.1.crt"
    if os.path.exists(pempath):
        if messagebox.askyesno(
            "上書確認",
            "証明書はすでに出力されています。上書きしてよろいですか？\n"
            "再出力の場合、固有のファイルの為、再インストールが必要です。\n"
            "インストール済みの方は「いいえ」を押して上書きをキャンセルしてください。\n",
        ):
            for file in glob.glob("*.crt"):
                os.remove(file)

            # f.close()
            # del f
            for file in glob.glob("*.key"):
                os.remove(file)
            for file in glob.glob("*.csr"):
                os.remove(file)
            for file in glob.glob("*.pem"):
                os.remove(file)
            for file in glob.glob("*.pfx"):
                os.remove(file)

        else:
            return


def generate_root_CA():
    """
    a) generate rootCA key
    b) generate rootCA crt
    """

    ##generating root key

    root_private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )

    ##self-sign and generate the root certificate

    root_c = Entry00.get() + "(self)CA"
    root_o = Entry04.get()
    root_ou = Entry05.get()

    root_public_key = root_private_key.public_key()
    builder = x509.CertificateBuilder()
    builder = builder.subject_name(
        x509.Name(
            [
                x509.NameAttribute(NameOID.COMMON_NAME, root_c),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, root_o),
                x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, root_ou),
            ]
        )
    )

    builder = builder.issuer_name(
        x509.Name(
            [
                x509.NameAttribute(NameOID.COMMON_NAME, root_c),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, root_o),
                x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, root_ou),
            ]
        )
    )

    builder = builder.not_valid_before(
        datetime.datetime.today() - datetime.timedelta(days=1)
    )
    builder = builder.not_valid_after(
        datetime.datetime.today() + datetime.timedelta(days=365 * 100)
    )
    builder = builder.serial_number(int(Serial))
    builder = builder.public_key(root_public_key)
    builder = builder.add_extension(
        x509.BasicConstraints(ca=True, path_length=None),
        critical=True,
    )

    root_certificate = builder.sign(
        private_key=root_private_key,
        algorithm=hashes.SHA256(),
        backend=default_backend(),
    )

    ##write to disk

    with open(root_c + ".key", "wb") as f:
        f.write(
            root_private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.BestAvailableEncryption(Password)
                # encryption_algorithm = serialization.BestAvailableEncryption(b"passphrase")
            )
        )

    with open(root_c + ".crt", "wb") as f:
        f.write(
            root_certificate.public_bytes(
                encoding=serialization.Encoding.PEM,
            )
        )

    return root_private_key, root_certificate


def generate_key():
    """
    a) generate key for the certificate being created
    """
    key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )

    with open("127.0.0.1.key", "wb") as f:
        f.write(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
                # encryption_algorithm=serialization.NoEncryption()
            )
        )
        f.close()

    with open("127.0.0.1_key.pem", "wb") as f:
        f.write(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
                # encryption_algorithm=serialization.NoEncryption()
            )
        )
        f.close()

    return key


def generate_csr(key, domain_name):
    """
    generate csr for the client certificate
    """
    domain_c = Entry01.get()
    domain_st = Entry03.get()
    domain_l = Entry02.get()
    domain_o = Entry04.get()
    domain_e = Entry06.get()

    csr = x509.CertificateSigningRequestBuilder().subject_name(
        x509.Name(
            [
                # Provide various details about who we are.
                x509.NameAttribute(NameOID.COUNTRY_NAME, domain_c),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, domain_st),
                x509.NameAttribute(NameOID.LOCALITY_NAME, domain_l),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, domain_o),
                x509.NameAttribute(NameOID.EMAIL_ADDRESS, domain_e),
                x509.NameAttribute(NameOID.COMMON_NAME, domain_name),
            ]
        )
    )

    # Sign the CSR with our private key.
    csr = csr.sign(key, hashes.SHA256(), default_backend())

    # Write our CSR out to disk.
    with open(domain_name + ".csr", "wb") as f:
        f.write(csr.public_bytes(serialization.Encoding.PEM))

    return csr


def sign_certificate_request(csr, rootkey, rootcrt, client_key, domain_name):
    """
    generate the certificate based on the csr created
    """
    san_list = []

    # uri = "*." + Entry07.get()
    # san_list.append(x509.DNSName(uri))
    uri = Entry07.get()
    if uri == "127.0.0.1":
        san_list.append(x509.DNSName("127.0.0.1"))
        san_list.append(x509.DNSName("::1"))
        san_list.append(x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")))
        san_list.append(x509.IPAddress(ipaddress.IPv6Address("::1")))

    if not uri == "127.0.0.1":
        # san_list.append(x509.DNSName('*:' + uri))
        san_list.append(x509.DNSName(uri))

    crt = (
        x509.CertificateBuilder()
        .subject_name(csr.subject)
        .issuer_name(rootcrt.subject)
        .public_key(csr.public_key())
        .serial_number(int(Serial) + 1)  # pylint: disable=no-member
        .not_valid_before(datetime.datetime.utcnow() - datetime.timedelta(days=1))
        .not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365 * 100)
        )
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_encipherment=True,
                content_commitment=True,
                data_encipherment=False,
                key_agreement=False,
                encipher_only=False,
                decipher_only=False,
                key_cert_sign=False,
                crl_sign=False,
            ),
            critical=True,
        )
        .add_extension(
            x509.ExtendedKeyUsage(
                [
                    ExtendedKeyUsageOID.CLIENT_AUTH,
                    ExtendedKeyUsageOID.SERVER_AUTH,
                    ExtendedKeyUsageOID.CODE_SIGNING,
                ]
            ),
            critical=True,
        )
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_public_key(rootkey.public_key()),
            critical=False,
        )
        .add_extension(x509.SubjectAlternativeName(san_list), critical=False)
        .sign(private_key=rootkey, algorithm=hashes.SHA256(), backend=default_backend())
    )
    # Extension=x509でエラー　X509のみに修正

    with open(domain_name + ".crt", "wb") as f:
        f.write(crt.public_bytes(encoding=serialization.Encoding.PEM))
    f.close()
    with open(domain_name + ".pem", "wb") as f:
        f.write(crt.public_bytes(encoding=serialization.Encoding.PEM))
    f.close()

    ct = crt
    create_pfx(client_key, ct)


def create_pfx(key: rsa.RSAPrivateKey, cert: x509.Certificate) -> bytes:
    p12 = pkcs12.serialize_key_and_certificates(
        name=b"",
        key=key,
        cert=cert,
        cas=None,
        # encryption_algorithm=NoEncryption(),
        encryption_algorithm=serialization.BestAvailableEncryption(Password),
    )

    with open("127.0.0.1.pfx", "wb") as f:
        f.write(p12)
    f.close()


def mycall():
    isPem()

    global Serial
    Serial = int(uuid.uuid4())
    domain_name = Entry07.get()

    global Password
    Password = bytes(Entry09.get(), encoding="utf-8", errors="replace")
    # print(Password)

    root_key, root_crt = generate_root_CA()
    domain_key = generate_key()
    csr = generate_csr(domain_key, domain_name)
    sign_certificate_request(csr, root_key, root_crt, domain_key, domain_name)

    """""
    with open(domain_name + ".key", 'wb') as f:
        f.write(domain_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
            #encryption_algorithm=serialization.NoEncryption()
        ))
        f.close()
 
 
        #with open('127.0.0.1.key', "r") as f:
        #    privkeydata = f.read()
        #with open('127.0.0.1.pem', 'r') as f:
        #    certdata = f.read()
 
        #cert = crypto.load_certificate(crypto.FILETYPE_PEM, certdata)
        #privkey = crypto.load_privatekey(crypto.FILETYPE_PEM, privkeydata)
        #p12 = crypto.PKCS12()
        #p12.set_privatekey(privkey)
        #p12.set_certificate(cert)
        ##p12data = p12.export(b"passphrase")
        #p12data = p12.export(Password)
        #with open('127.0.0.1.pfx', 'wb') as pfxfile:
        #    pfxfile.write(p12data)
        """

    if messagebox.askyesno(
        "出力完了",
        "出力した証明書をWindowsの証明書ストアにインストールしますか？\n"
        "「証明書をすべて次のストアに配置する＞証明書を信頼されたルートの証明期間」にインストールしてください\n"
        "IE,Edge,Chromeの方は「はい」を押してください。FireFoxはWindowsの証明書ストアを参照しませんので「いいえ」を押してください\n"
        "＊インストール後、再度出力すると、前回とは違うKEYが出力されます。ご注意ください。",
    ):
        subprocess.Popen(["start", "./" + Entry00.get() + "(self)CA.crt"], shell=True)

        # messagebox.showinfo('出力完了', '再度出力すると乱数とパスワードを使ってますので、違うシリアルのKEYが出力されます。ご注意ください。')

    else:
        # messagebox.showinfo('出力は完了しました。',
        if messagebox.askyesno(
            "証明書出力完了しましたがインストールはしていません",
            "証明書を削除しますか？\n"
            "FireFoxの方は「いいえ」を押し手動で「"
            + Entry00.get()
            + "(self)CA.crt」をFirefoxへ手動インストールしてください。\n"
            "インストールしない場合は「はい」をおしてください\n"
            "フォルダにある「"
            + Entry00.get()
            + "(self)CA.crt」「127.0.0.1.pem」「127.0.0.1.csr」「127.0.0.1.crt」「127.0.0.1.key」を削除します。\n"
            ""
            ""
            "",
        ):
            for file in glob.glob("*.crt"):
                os.remove(file)

            # f.close()
            # del f
            for file in glob.glob("*.key"):
                os.remove(file)
            for file in glob.glob("*.csr"):
                os.remove(file)
            for file in glob.glob("*.pem"):
                os.remove(file)
            for file in glob.glob("*.pfx"):
                os.remove(file)
    exit()


root = tk.Tk()
root.title("SSL_Maker")
root.geometry("230x260")
root.iconbitmap(default="sk.ico")
# root.iconphoto(False, tk.PhotoImage(file='sr47.png'))
# root.iconify()

Label00 = tk.Label(root, text="認証局名", fg="Blue")
Label00.grid(row=0, column=0, columnspan=2)
Entry00 = tk.Entry()
Entry00.grid(row=0, column=3, columnspan=2)
Entry00.insert(tk.END, "UnPySide")


Label01 = tk.Label(root, text="国", fg="Blue")
Label01.grid(row=1, column=0, columnspan=2)

Entry01 = tk.Entry()
Entry01.grid(row=1, column=3, columnspan=2)
Entry01.insert(tk.END, "JP")

Label02 = tk.Label(root, text="都道府県", fg="Blue")
Label02.grid(row=2, column=0, columnspan=2)

Entry02 = tk.Entry()
Entry02.grid(row=2, column=3, columnspan=2)
Entry02.insert(tk.END, "Osaka")

Label03 = tk.Label(root, text="市町村", fg="Blue")
Label03.grid(row=3, column=0, columnspan=2)

Entry03 = tk.Entry()
Entry03.grid(row=3, column=3, columnspan=2)
Entry03.insert(tk.END, "Osaka-shi")


Label04 = tk.Label(root, text="組織名", fg="Blue")
Label04.grid(row=4, column=0, columnspan=2)

Entry04 = tk.Entry()
Entry04.grid(row=4, column=3, columnspan=2)
Entry04.insert(tk.END, "UnPySide")

Label05 = tk.Label(root, text="ユニット名", fg="Blue")
Label05.grid(row=5, column=0, columnspan=2)

Entry05 = tk.Entry()
Entry05.grid(row=5, column=3, columnspan=2)
Entry05.insert(tk.END, "UnPySide")

Label06 = tk.Label(root, text="メアド", fg="Blue")
Label06.grid(row=6, column=0, columnspan=2)

Entry06 = tk.Entry()
Entry06.grid(row=6, column=3, columnspan=2)
Entry06.insert(tk.END, "unpyside@gmail.com")

Label07 = tk.Label(root, text="LoclPort(変更不可)", fg="Blue")
Label07.grid(row=7, column=0, columnspan=2)

Entry07 = tk.Entry()
Entry07.grid(row=7, column=3, columnspan=2)

Entry07.configure(state="normal")
Entry07.insert(tk.END, "127.0.0.1")
Entry07.configure(state="readonly")


Label08 = tk.Label(root, text="WebAddress", fg="Blue")
Label08.grid(row=8, column=0, columnspan=2)

Entry08 = tk.Entry()
Entry08.grid(row=8, column=3, columnspan=2)
Entry08.insert(tk.END, "https://unpyside.com")

Label09 = tk.Label(root, text="Password", fg="Blue")
Label09.grid(row=9, column=0, columnspan=2)

Entry09 = tk.Entry()
Entry09.grid(row=9, column=3, columnspan=2)
Entry09.insert(tk.END, "un")


Label11 = tk.Label(root, text="個人情報は入力しないでください。", fg="Red")
Label11.grid(row=11, column=0, columnspan=4)
Button001 = tk.Button(
    root,
    text="  証明書「crt」「key」ファイル出力  ",
    font="Helvetica 9 bold",
    bg="#f0e68c",
    fg="Green",
    command=mycall,
)
Button001.grid(row=12, column=0, columnspan=4)

root.mainloop()
