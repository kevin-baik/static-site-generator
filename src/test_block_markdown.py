import unittest
from block_markdown import(
    BlockType,
    markdown_to_blocks,
    block_to_block_type
)

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_block_to_block_type(self):
        blocks = [
            "### Heading 3",
            "``` Code Red ```",
            ">quote1\n>quote2\n>quote3",
            "- item1\n- item2\n- item3",
            "1. rank1\n2. rank2\n 3. rank3",
            "This is a simple PARAGRAPH."
        ]
        test_result = []
        for block in blocks:
            test_result.append(block_to_block_type(block))
        self.assertEqual(
            test_result,
            [
                BlockType.HEADING,
                BlockType.CODE,
                BlockType.QUOTE,
                BlockType.UNORDERED_LIST,
                BlockType.ORDERED_LIST,
                BlockType.PARAGRAPH
            ]
        )

if __name__ == "__main__":
    unittest.main()
