from textnode import TextNode, TextType
def main():
    node = TextNode("some text", TextType.BOLD, "https://forums.somethingawful.com")
    print(node)

if __name__ == "__main__":
    main()
