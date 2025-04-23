import os
import subprocess
import mammoth
import tempfile
import shutil


def wps_to_docx(wps_path):
    """
    将WPS文件转换为DOCX格式 - 使用LibreOffice直接转换
    """
    # 检查文件是否存在
    if not os.path.exists(wps_path):
        raise FileNotFoundError(f"找不到文件: {wps_path}")

    # 创建临时目录用于存放转换后的docx文件
    temp_dir = tempfile.mkdtemp()

    # 获取绝对路径（解决相对路径问题）
    abs_wps_path = os.path.abspath(wps_path)

    try:
        # 使用LibreOffice命令行直接转换
        cmd = [
            'libreoffice', '--headless', '--convert-to', 'docx',
            '--outdir', temp_dir, abs_wps_path
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        # 构建输出的docx文件路径
        file_name = os.path.splitext(os.path.basename(wps_path))[0]
        docx_path = os.path.join(temp_dir, f"{file_name}.docx")

        # 检查转换后的文件是否存在
        if not os.path.exists(docx_path):
            raise Exception(f"转换失败，无法找到输出文件: {docx_path}")

        return docx_path
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.decode('utf-8', errors='ignore')
        raise Exception(f"LibreOffice转换失败: {str(e)}, 错误输出: {stderr}")


def docx_to_markdown(docx_path):
    """
    将DOCX文件转换为Markdown

    参数:
    docx_path: DOCX文件路径

    返回:
    markdown_content: Markdown格式的内容
    """
    # 检查文件是否存在
    if not os.path.exists(docx_path):
        raise FileNotFoundError(f"找不到文件: {docx_path}")

    try:
        # 打开docx文件
        with open(docx_path, "rb") as docx_file:
            # 使用mammoth将docx转换为markdown
            result = mammoth.convert_to_markdown(docx_file)
            markdown_content = result.value

            return markdown_content
    except Exception as e:
        raise Exception(f"Markdown转换失败: {str(e)}")


def wps2md(wps_path, output_path=None):
    """
    将WPS文件转换为Markdown格式

    参数:
    wps_path: WPS文件路径
    output_path: Markdown文件保存路径（可选）

    返回:
    markdown_content: Markdown格式的内容
    output_path: Markdown文件保存路径
    """
    try:
        # 将WPS转换为DOCX
        docx_path = wps_to_docx(wps_path)

        # 将DOCX转换为Markdown
        markdown_content = docx_to_markdown(docx_path)

        # 如果没有指定输出路径，则使用和原文件相同的名称和位置
        if output_path is None:
            dir_name = os.path.dirname(wps_path)
            file_name = os.path.splitext(os.path.basename(wps_path))[0]
            output_path = os.path.join(dir_name, f"{file_name}.md")

        # 将Markdown内容保存到文件
        with open(output_path, 'w', encoding='utf-8') as md_file:
            md_file.write(markdown_content)

        # 清理临时文件
        if os.path.exists(os.path.dirname(docx_path)):
            shutil.rmtree(os.path.dirname(docx_path))

        return markdown_content, output_path

    except Exception as e:
        # 确保清理临时文件
        if 'docx_path' in locals() and os.path.exists(os.path.dirname(docx_path)):
            shutil.rmtree(os.path.dirname(docx_path))
        raise Exception(f"WPS转MD失败: {str(e)}")