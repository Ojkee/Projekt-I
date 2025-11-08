class ParserErrorUserMsg:
    @staticmethod
    def illegal_str(illegal: str) -> str:
        return f"Illegal character: {illegal}"

    @staticmethod
    def extra_input_in_line(next_str: str) -> str:
        return f"Extra character: {next_str} after the expression. Maybe move to next line?"
