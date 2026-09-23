from flask import (
    Flask,
    render_template, 
    request,
    redirect,
    session,
    url_for
)

from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

app = Flask(__name__)

# Secret Key
app.config["SECRET_KEY"] = "rahasia123"

# Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ==========================
# DATABASE USER
# ==========================

class User(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="user"
    )


# ==========================
# DATABASE PRODUK
# ==========================

class Product(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nama = db.Column(
        db.String(100),
        nullable=False
    )

    harga = db.Column(
        db.Integer,
        nullable=False
    )

    kategori = db.Column(
        db.String(50),
        nullable=False
    )

    gambar = db.Column(
        db.String(255),
        nullable=True
    )


# ==========================
# MEMBUAT DATABASE
# ==========================

with app.app_context():
    db.create_all()


# ==========================
# HALAMAN UTAMA
# ==========================

@app.route("/")
@app.route("/dashboard")
def home():
    
    makanan = Product.query.filter_by(kategori="Makanan").all()
    minuman = Product.query.filter_by(kategori="Minuman").all()

    return render_template(
        "dashboard.html",
        makanan=makanan,
        minuman=minuman
    )


# ==========================
# LOGIN
# ==========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Login Admin
        if username == "admin" and password == "admin123":

            session["username"] = "admin"
            session["role"] = "admin"

            return redirect("/admin")

        # Login User
        user = User.query.filter_by(
            username=username
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            session["username"] = user.username
            session["role"] = user.role

            return redirect("/")

        return "Username atau password salah."

    return render_template("login.html")


# ==========================
# REGISTER
# ==========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Password tidak sama
        if password != confirm_password:
            return "Konfirmasi password tidak sama."

        # Username sudah dipakai
        user = User.query.filter_by(
            username=username
        ).first()

        if user:
            return "Username sudah digunakan."

        # Simpan user
        user_baru = User(
            username=username,
            password=generate_password_hash(password),
            role="user"
        )

        db.session.add(user_baru)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")


# ==========================
# ADMIN
# ==========================

@app.route("/admin")
def dashboard():

    if session.get("role") != "admin":
        return redirect("/")

    products = Product.query.all()

    return render_template(
        "admin.html",
        products=products
    )



@app.route("/hapus-produk/<int:id>")
def hapus_produk(id):

    if session.get("role") != "admin":
        return redirect("/")

    produk = Product.query.get_or_404(id)

    db.session.delete(produk)
    db.session.commit()

    return redirect("/admin")



@app.route("/tambah-produk", methods=["POST"])
def tambah_produk():

    if session.get("role") != "admin":
        return redirect("/")

    nama = request.form["nama"]
    harga = request.form["harga"]
    kategori = request.form["kategori"]

    produk = Product(
        nama=nama,
        harga=int(harga),
        kategori=kategori
    )

    db.session.add(produk)
    db.session.commit()

    return redirect("/admin")
    
    
    
# ==========================
# EDIT PRODUK
# ==========================

@app.route("/edit-produk/<int:id>")
def edit_produk(id):
    
    produk = Product.query.get_or_404(id)
    
    return render_template("edit.html", produk=produk)



@app.route("/update-produk/<int:id>", methods=["POST"])
def update_produk(id):
    
    produk = Product.query.get_or_404(id)
    
    produk.nama = request.form["nama"]
    produk.harga = int(request.form["harga"])
    produk.kategori = request.form["kategori"]
    
    db.session.commit()
    
    return redirect("/admin")

# ==========================
# KATEGORI
# ==========================

@app.route("/kategori/<kategori>")
def kategori(kategori):
    
    products = Product.query.filter_by(kategori=kategori).all()
    
    return  render_template("dashboard.html" , 
    products=products, 
    kategori=kategori
    )


# ==========================
# LOGOUT
# ==========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ==========================
# MENJALANKAN FLASK
# ==========================

if __name__ == "__main__":

    app.run(
        debug=True
    )