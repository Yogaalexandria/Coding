from flask import Flask, jsonify, request, send_file

app = Flask(__name__)

PRICES = {
    "apel": 12000,
    "jeruk": 9000,
    "pisang": 7000,
}
DISCOUNT_THRESHOLD = 50000
DISCOUNT_RATE = 0.10


def calculate_order(data):
    if not isinstance(data, dict):
        raise ValueError("Data pesanan tidak valid.")

    items = {}
    for item_name, unit_price in PRICES.items():
        quantity = data.get(item_name, 0)
        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            raise ValueError(f"Jumlah {item_name} harus berupa angka.")

        if quantity < 0:
            raise ValueError(f"Jumlah {item_name} tidak boleh negatif.")

        items[item_name] = quantity

    subtotal = sum(items[name] * price for name, price in PRICES.items())
    discount = subtotal * DISCOUNT_RATE if subtotal >= DISCOUNT_THRESHOLD else 0
    total = subtotal - discount

    return {
        "items": items,
        "subtotal": subtotal,
        "discount": discount,
        "total": total,
        "discount_applied": subtotal >= DISCOUNT_THRESHOLD,
    }


@app.route("/")
def index():
    return send_file("main.html")


@app.route("/checkout", methods=["POST"])
def checkout():
    payload = request.get_json(silent=True) or {}

    try:
        result = calculate_order(payload)
        return jsonify({"success": True, **result})
    except ValueError as exc:
        return jsonify({"success": False, "message": str(exc)}), 400


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


def run_cli():
    print("Selamat datang di Yoga Shop")
    print("Selamat Berbelanja!")

    buah = {}
    for nama in PRICES:
        while True:
            try:
                jumlah = int(input(f"Masukkan jumlah {nama}: "))
                if jumlah < 0:
                    print("Jumlah tidak boleh negatif. Silakan coba lagi.")
                    continue
                buah[nama] = jumlah
                break
            except ValueError:
                print("Input tidak valid. Masukkan angka bulat.")

    result = calculate_order(buah)
    print("\nRincian pesanan:")
    for nama, jumlah in result["items"].items():
        print(f"- {nama.title()}: {jumlah} buah x Rp{PRICES[nama]:,}")

    if result["discount_applied"]:
        print(f"Diskon 10% berhasil diterapkan: Rp{result['discount']:,}")
    else:
        print("Belum mencapai minimum diskon. Total pembelian belum mendapat potongan.")

    print(f"Subtotal: Rp{result['subtotal']:,}")
    print(f"Total akhir: Rp{result['total']:,}")
    print("Terima kasih sudah berbelanja di Yoga Shop!")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
