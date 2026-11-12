import fitz

from .config import SAMPLE_PDF, OUTPUT_DIR


def convert_pdf_pages_to_images(file_path):
    output_folder = OUTPUT_DIR / "Rendered_Pages"
    output_folder.mkdir(parents=True, exist_ok=True)

    document = fitz.open(file_path)

    for page_number, page in enumerate(document, start=1):
        pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        output_file = output_folder / f"Page_{page_number}.png"
        pixmap.save(output_file)
        print("Page image created:", output_file.name)

    document.close()


def extract_embedded_images(file_path):
    output_folder = OUTPUT_DIR / "Extracted_Images"
    output_folder.mkdir(parents=True, exist_ok=True)

    document = fitz.open(file_path)
    image_count = 0

    for page_number, page in enumerate(document, start=1):
        images = page.get_images(full=True)

        for image_info in images:
            image_count += 1
            image_data = document.extract_image(image_info[0])

            extension = image_data["ext"]
            output_file = (
                output_folder /
                f"Page_{page_number}_Image_{image_count}.{extension}"
            )

            with open(output_file, "wb") as file:
                file.write(image_data["image"])

            print("Extracted image:", output_file.name)

    document.close()
    print("Total embedded images:", image_count)


if __name__ == "__main__":
    convert_pdf_pages_to_images(SAMPLE_PDF)
    extract_embedded_images(SAMPLE_PDF)