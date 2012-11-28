import os
from PIL import Image, ImageDraw

class FontDef:
    def __init__(self, name, from_path, to_path):
        self.name = name
        self.from_path = from_path
        self.to_path = to_path

        self.lineHeight = 0
        self.base = 0
        self.chars = []
        self.image = None
        
        lines = open(os.path.join(from_path, '%s.fnt' % name)).readlines()

        for line in lines:
            self.parse_line(line)

    def parse_line(self, line):
        line = line.replace('".*"', '')
        segs = line.split(' ')
        cmd = segs[0]
        if cmd == 'info':
            return

        params = '{"' + ',"'.join([a.replace('=', '":') for a in segs[1:]]) + '}'
        params = eval(params)
        self.parse_cmd(cmd, params)
        
    def parse_cmd(self, cmd, params):
        if cmd == 'common':
            self.lineHeight = int(params['lineHeight'])
            self.base = int(params['base'])
        elif cmd == 'page':
            self.image = Image.open(os.path.join(self.from_path, params['file']))
        elif cmd == 'char':
            self.chars.append(params)

    def convert(self):
        self.convert_gxfont()
        self.convert_vga()

    def convert_gxfont(self):
        lines = []
        lines.append('CIwGxFont')
        lines.append('{')
        lines.append('    utf8 1')
        lines.append('    image %s.tga' % self.name)
        charmap = ''
        for ch in self.chars:
            charmap = charmap + unichr(int(ch['id']))

        lines.append('    charmap "%s"' % charmap.replace('"', '\\"').encode('utf-8'))
        lines.append('}')

        f = open(os.path.join(self.to_path, '%s.gxfont' % self.name), 'w')
        f.write('\n'.join(lines))
        f.close()
   
    def convert_vga(self):
        margin = 3
        width = margin
        maxHeight = self.lineHeight
        for ch in self.chars:
            w = max(int(ch['width']) + int(ch['xoffset']), int(ch['xadvance']))
            width += w + margin
            h = int(ch['height']) - int(ch['yoffset'])
            maxHeight = max(maxHeight, h)

        height = maxHeight + margin * 2
        tga = Image.new('RGBA', (width, height))
        draw = ImageDraw.Draw(tga)
        draw.rectangle((0,0,width, height), 'black')

        targetX = margin
        for ch in self.chars:
            x = int(ch['x'])
            y = int(ch['y'])
            w = int(ch['width'])
            h = int(ch['height'])
            xoffset = int(ch['xoffset'])
            targetW = max(w + xoffset, int(ch['xadvance']))
            draw.rectangle((targetX, margin, targetX + targetW, margin + maxHeight), (0,0,0,0))

            glyph = self.image.copy().crop((x, y, x + w, y + h))
            targetY = margin + int(ch['yoffset']) + (self.lineHeight - self.base) / 2
            target = (targetX + xoffset, targetY, targetX + xoffset + w, targetY + h)
            tga.paste(glyph, target)
            targetX += targetW + margin

        tga.save(os.path.join(self.to_path, '%s.tga' % self.name), format='TGA')

