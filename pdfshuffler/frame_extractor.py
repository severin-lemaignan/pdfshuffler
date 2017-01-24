import re


class FrameExtractor:

    def get_until_closing_brace(self, text):
        openning = 0
        for i in range(len(text)):
            if text[i] == "{":
                openning += 1
            if text[i] == "}":
                openning -= 1
            if openning == 0:
                return text[0:i+2], text[i+3:]

        raise Exception("No closing brace!!")
        
    def get_next_frame(self, text):
        lines = text.splitlines(True)

        if     lines[0].strip().startswith("\\imageframe") \
            or lines[0].strip().startswith("\\videoframe") \
            or lines[0].strip().startswith("\\licenseframe") \
            or lines[0].strip().startswith("\\maketitle") \
            or lines[0].strip().startswith("\\section"):
            return lines[0], "".join(lines[1:])

        frame_txt = ""

        if lines[0].strip().startswith("\\begin{frame}"):
            i=0
            while "\\end{frame}" not in lines[i]:
                frame_txt += lines[i]
                i += 1
            frame_txt += lines[i]
            return frame_txt, "".join(lines[i+1:])

        if lines[0].strip().startswith("{"):
            inbrace, rest = self.get_until_closing_brace(text)
            if not "frame" in inbrace:
                return None, text
            if inbrace.count("begin{frame") == 1 or inbrace.count("\\frame") == 1:
                return inbrace, rest
            
            # more difficult case: several frames are enclosed in { ... }
            # extract just one frame, and copy the preamble in front of the next one (returned in the 'rest')
            preamble = ""
            framegroup = inbrace.splitlines(True)
            i=0
            while not "\\begin{frame}" in framegroup[i]:
                frame_txt += framegroup[i]
                preamble += framegroup[i]
                i += 1
            while "\\end{frame}" not in lines[i]:
                frame_txt += framegroup[i]
                i += 1
            frame_txt += framegroup[i]
            frame_txt += framegroup[-1]

            return frame_txt, "\n" + preamble + "".join(framegroup[i+1:]) + rest

        return None, text


    def load_latex(self, texfile):

        self.frames = []

        with open(texfile,'r') as f:

            preamble = ""
            footer = ""
            preamble_done = False
            lines = f.readlines()
            i = 0
            while True:
                if not "frame" in lines[i] and not preamble_done:
                    preamble += lines[i]
                    i += 1
                else:
                    preamble_done = True

                    frame, rest = self.get_next_frame("".join(lines[i:]))

                    if frame:
                        self.frames.append(frame)
                        i += len(frame.splitlines())
                        footer = rest
                        lines = rest.splitlines(True)
                        i = 0
                    else:
                        i += 1

                    if i >= len(lines):
                        break

                self.header = preamble
                self.footer = footer



if __name__ == "__main__":

    extractor = FrameExtractor()
    extractor.load_latex("/home/skadge/talks/presentation-cognitive-robotics/presentation.tex")

    for idx, frame in enumerate(extractor.frames):
        print("Frame %s" % (idx + 1))
        print("-------------------")
        print(frame)
        print("-------------------")

