import io
import base64
from PIL import Image
import qrcode
from qrcode.image.svg import SvgPathImage


class QRService:

    @staticmethod
    def generate_qr(
        text: str,
        size: int = 200,
        fg_color: str = "#000000",
        bg_color: str = "#FFFFFF",
        logo_b64: str | None = None,
        output_format: str = "png",
    ) -> bytes:
        qr = qrcode.QRCode(box_size=10, border=4)
        qr.add_data(text)
        qr.make(fit=True)

        if output_format == "svg":
            img = qr.make_image(
                image_factory=SvgPathImage,
                fill_color=fg_color,
                back_color=bg_color,
            )
            return img.to_string()

        img = qr.make_image(fill_color=fg_color, back_color=bg_color)
        img = img.convert("RGBA")
        img = img.resize((size, size), Image.NEAREST)

        if logo_b64:
            try:
                logo_data = base64.b64decode(logo_b64)
                logo_img = Image.open(io.BytesIO(logo_data)).convert("RGBA")
                logo_max = size // 4
                logo_w, logo_h = logo_img.size
                if logo_w > logo_max or logo_h > logo_max:
                    ratio = min(logo_max / logo_w, logo_max / logo_h)
                    logo_w, logo_h = int(logo_w * ratio), int(logo_h * ratio)
                    logo_img = logo_img.resize(
                        (logo_w, logo_h), Image.LANCZOS
                    )
                pos = ((size - logo_w) // 2, (size - logo_h) // 2)
                img.paste(logo_img, pos, logo_img)
            except Exception:
                pass

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()

    @staticmethod
    def generate_qr_b64(
        text: str,
        size: int = 200,
        fg_color: str = "#000000",
        bg_color: str = "#FFFFFF",
        logo_b64: str | None = None,
        output_format: str = "png",
    ) -> str:
        raw = QRService.generate_qr(text, size, fg_color, bg_color, logo_b64, output_format)
        return base64.b64encode(raw).decode()
