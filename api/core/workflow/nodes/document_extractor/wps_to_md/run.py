import os
from wps2md import wps2md


def main():
    """
    主函数，用于调用wps2md转换功能，使用固定路径
    """
    try:
        # 使用硬编码的文件路径
        wps_file_path = "file/2024-10413 佛山市全面推行林长制工作领导小组办公室关于协助做好绿美佛山生态建设信息报送工作的通知.wps"
        output_dir = "output"

        # 确保输出目录存在
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 构建输出文件路径
        file_name = os.path.splitext(os.path.basename(wps_file_path))[0]
        output_path = os.path.join(output_dir, f"{file_name}.md")

        # 调用wps2md函数进行转换
        markdown_content, saved_path = wps2md(wps_file_path, output_path)

        print(f"转换成功！")
        print(f"Markdown内容预览: \n{markdown_content[:200]}...")
        print(f"Markdown文件已保存到: {saved_path}")

    except Exception as e:
        print(f"转换失败: {str(e)}")


if __name__ == "__main__":
    main()