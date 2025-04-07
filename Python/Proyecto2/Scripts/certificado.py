from PIL import Image, ImageDraw, ImageFont
import os

def crear_certificado(nombre, output_path="certificado.png"):
    dir = os.path.dirname(os.path.abspath(__file__))
    width, height = 1200, 800
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    try:
        font_path = os.path.join(os.path.dirname(dir),"Resources\Montserrat-Bold.ttf")
        font = ImageFont.truetype(font_path, 20)
    except:
        font = ImageFont.load_default()
        print("Montserrat font not found, using default font")
    
    title = "CERTIFICADO"
    title_font = ImageFont.truetype(font_path, 40) if "font_path" in locals() else ImageFont.load_default()
    title_width = draw.textlength(title, font=title_font)
    draw.text(((width - title_width)/2, 50), title, fill="black", font=title_font)
    
    text = (
        f"Se certifica que {nombre} ha completado con éxito el\n"
        "Programa de capacitación que aplica algoritmos de grafos\n"
        "para la conservación de bosques.\n"
        "\n"
        f"Por medio de este documento se le otorga el titulo a {nombre} como:\n"
        "'Guardian del Bosque'"
    )
    
    lines = text.split('\n')
    y_position = 200
    
    for line in lines:
        line_width = draw.textlength(line, font=font)
        x_position = (width - line_width) / 2
        draw.text((x_position, y_position), line, fill="black", font=font)
        y_position += 30 
    
    draw.rectangle([50, 50, width-50, height-50], outline="gold", width=5)
    
    footer = "© 2025 Programa Guardianes del Bosque"
    footer_font = ImageFont.truetype(font_path, 16) if "font_path" in locals() else ImageFont.load_default()
    footer_width = draw.textlength(footer, font=footer_font)
    draw.text(((width - footer_width)/2, height-80), footer, fill="gray", font=footer_font)
    
    image.save(output_path)
    print(f"Certificado guardado como {output_path}")
