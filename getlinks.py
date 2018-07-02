import fitz      # = PyMuPDF
from os import path

from test_line import parse_line

g_toc = []


def match_string(src, patten):
    i = src.find(patten)
    if i is not -1:
        #print("find")
        pass
    else:
        pass
        #print("not find")

    return i

def find_toc_start_page(doc):
    total_page = doc.pageCount
    print("docs total page: ", total_page)
    total_page = 20
    c_page_n = 0
    toc_page_start = -1
    toc_page_end = -1
    while c_page_n < total_page:
        page = doc.loadPage(c_page_n)

        tt = page.getText(output='text')
        '''
        print("----------   ", "start: ", c_page_n, "  ---------" )
        print(tt)
        print("----------   ", " end:  ", c_page_n, "  ---------\n")
        '''
        toc_start = match_string(tt, '\nTable of Contents')
        if toc_start is not -1:
            toc_page_start = c_page_n
            break
        c_page_n += 1

    '''
    To compute the ToC end page
    '''

    '''
    while c_page_n < total_page:
        page = doc.loadPage(c_page_n)
        toc_page_end

    print("Toc: {} - {}".format(toc_page_start, toc_page_end))
    '''
    return toc_page_start


def get_text_of_line(l):
    #print(" start to cancatenate string:")
    str = ''
    for s in l['spans']:
        #print("   span text is: [{}]".format(s['text']))
        str += (s['text'])

    if str is not '':
        pass
        #print(" result: [{}]".format(str))

    return str


def do_overview():
    toc = doc.getToC()                               # get current table of contents
    for t in toc:
        print(t)

    page = doc.loadPage(page_start)
    print("page content: {}".format(page))
    links = page.getLinks()
    print("links: {}".format(links))

    for ln in links:
        if ln["kind"] == fitz.LINK_GOTO:
            print("Jump to page", ln["page"] + 1, ln)
        elif ln["kind"] in (fitz.LINK_GOTOR, fitz.LINK_LAUNCH):
            print("Open or launch file", ln["file"])
        elif ln["kind"] == fitz.LINK_URI:
            print("Open URI", ln["uri"])


    tt = page.getText(output='text')
    td = page.getText(output='dict')

    print(tt)
    print(td['blocks'][0])
    for i in td['blocks']:
        if i['type'] == 0:
            print("type is {}, length: {} and {}".format(i['type'], len(i['lines']), i['bbox']))
            if len(i['lines']) == 3:
                print("lens:{}".format(i['lines'][0]))
                print("lens:{}".format(i['lines'][1]))
                print("lens:{}".format(i['lines'][2]))

                label = i['lines'][0]['spans'][0]['text']
                pos = i['lines'][0]['bbox']
                print(label, pos)

    '''
    type is 0, length: 3 and [54.0, 712.4681396484375, 473.59503173828125, 725.9760131835938]
    lens:{'dir': (1.0, 0.0), 'spans': [{'font': 'Segoe UI,Bold', 'size': 9.960000038146973, 'text': 'Aggregate Perf Counter A9 Upper DWord ', 'flags': 16}], 'wmode': 0, 'bbox': (54.0, 712.4681396484375, 252.87896728515625, 725.7157592773438)}
    lens:{'dir': (1.0, 0.0), 'spans': [{'font': 'Segoe UI,Bold', 'size': 9.960000038146973, 'text': '............................................................................... ', 'flags': 16}], 'wmode': 0, 'bbox': (250.85000610351562, 712.4681396484375, 462.178955078125, 725.7157592773438)}
    lens:{'dir': (1.0, 0.0), 'spans': [{'font': 'Segoe UI,Bold', 'size': 9.960000038146973, 'text': '33', 'flags': 16}, {'font': 'Calibri', 'size': 11.039999961853027, 'text': ' ', 'flags': 0}], 'wmode': 0, 'bbox': (459.54998779296875, 712.4681396484375, 473.59503173828125, 725.9760131835938)}

    '''

    print("hello----------------------------------")
    items = get_item(page)
    for i in items:
        print(i['label'], i['pos'])

    hylinks = get_links(page)
    for i in hylinks:
        print(i['page'], i['pos'])


    for i in hylinks:
        for j in items:
            # if i['pos'].intersect(j['pos']):
            #    print("True: ", j['label'],i['page'])
            if match(i['pos'], j['pos']):
                print("compare: ", j['pos'][0], i['page'], i['pos'], j['label'], j['pos'], )
                break



def get_links(page):
    items = []

    links = page.getLinks()

    for ln in links:
        if ln["kind"] == fitz.LINK_GOTO:
            # print("Jump to page", ln["page"] + 1, ln)
            pass
            items.append({'page': ln["page"] + 1, 'pos': ln["from"]})
        elif ln["kind"] in (fitz.LINK_GOTOR, fitz.LINK_LAUNCH):
            pass
            #print("Open or launch file", ln["file"])
        elif ln["kind"] == fitz.LINK_URI:
            pass
            #print("Open URI", ln["uri"])

    return items

def get_item(page):
    item = []

    td = page.getText(output='dict')
    for i in td['blocks']:
        if i['type'] == 0 and len(i['lines']) == 3:
            label = i['lines'][0]['spans'][0]['text']
            pos = i['lines'][0]['bbox']
            print(label, pos)

            item.append({'label': label, 'pos': pos})


    return item




def match(rect1, rect2):
    r = fitz.Rect(rect2[0], rect2[1], rect2[2], rect2[3])
    #b = rect1.contains(r)  # doesn't work
    b = rect1.intersects(r)
    return b


def update_level():
    l = [r[0] for r in g_toc]
    s = sorted(set(l))

    for j, vv in enumerate(l):
        for k, v in enumerate(s):
            if vv == v:
                l[j] = vv - v + k + 1
                g_toc[j][0] = l[j]
                break
    pass


def gen_toc(page):
    items = get_item(page)
    # for i in items:
    #     print(i['label'], i['pos'])

    hylinks = get_links(page)
    # for i in hylinks:
    #     print(i['page'], i['pos'])

    for i in hylinks:
        for j in items:
            # if i['pos'].intersect(j['pos']):
            #    print("True: ", j['label'],i['page'])
            if match(i['pos'], j['pos']):
                print("compare: ", j['pos'][0], i['page'], i['pos'], j['label'], j['pos'], )
                g_toc.append([int(j['pos'][0]), j['label'], i['page']])
                break


def rect_is_match_test():
    r1_link = fitz.Rect(51.75, 133.42999267578125, 473.25, 152.72998046875)
    r2_text = fitz.Rect(54.0, 133.3921661376953, 192.24896240234375, 146.63973999023438)

    print(r1_link.intersects(r2_text))


#do_overview()

def do_merge_1_line(td):
    '''
    page = doc.loadPage(0)
    td = page.getText(output='dict')
    '''
    do_merge_1_line = False
    lines = []  # {'bbox': (x1, y1, x2, y2), 'text': 'Item .... 10' }

    for b in td['blocks']:
        if b['type'] == 0:

            if do_merge_1_line:
                print("type is {}, length: {} and {}".format(b['type'], len(b['lines']), b['bbox']))

            for l in b['lines']:

                s = get_text_of_line(l)
                t = {'bbox': l['bbox'], 'text': s}

                if len(lines) == 0:
                    pass
                else:
                    pass
                lines.append(t)

    return lines

def do_is_same_line(b1, b2):
    '''
     b1.y1 == b2.y1 ==> in the same line
     Need to improve it

    :param b1:
    :param b2:
    :return:
    '''
    if b1[1] == b2[1]:
        return True
    else:
        return False
    pass

def do_show_lines():
    pass
    page = doc.loadPage(page_start)
    # links = page.getLinks()
    # print("links: {}".format(links))
    #
    # for ln in links:
    #     if ln["kind"] == fitz.LINK_GOTO:
    #         print("Jump to page", ln["page"] + 1, ln)
    #     elif ln["kind"] in (fitz.LINK_GOTOR, fitz.LINK_LAUNCH):
    #         print("Open or launch file", ln["file"])
    #     elif ln["kind"] == fitz.LINK_URI:
    #         print("Open URI", ln["uri"])

    tt = page.getText(output='text')
    print(tt)
    td = page.getText(output='dict')

    lines = do_merge_1_line(td)

    print('-----------')
    for i in lines:
        print(i['bbox'], i['text'])
    print('-----------')


    toc_lines = []
    toc_lines_cur_number = -1
    flag_new_line = True

    for i in lines:
        if flag_new_line is True:
            toc_lines.append(i)
            toc_lines_cur_number +=1
            flag_new_line = False
        else:
            YisEqual = do_is_same_line(toc_lines[toc_lines_cur_number]['bbox'], i['bbox'])
            if YisEqual is True:
                toc_lines[toc_lines_cur_number]['text'] += i['text']
            else:
                toc_lines.append(i)
                toc_lines_cur_number += 1
                flag_new_line = False

    print('------------')
    for i in toc_lines:
        print(i['bbox'], parse_line(i['text']))
    print('-----------')


def toc_in_page(doc, n):
    page = doc.loadPage(n)

    td = page.getText(output='dict')

    lines = do_merge_1_line(td)

    print_lines = False
    if print_lines:
        print('-----------')
        for i in lines:
            print(i['bbox'], i['text'])
        print('-----------')

    toc_lines = []
    toc_lines_cur_number = -1
    flag_new_line = True

    for i in lines:
        if flag_new_line is True:
            toc_lines.append(i)
            toc_lines_cur_number +=1
            flag_new_line = False
        else:
            YisEqual = do_is_same_line(toc_lines[toc_lines_cur_number]['bbox'], i['bbox'])
            if YisEqual is True:
                toc_lines[toc_lines_cur_number]['text'] += i['text']
            else:
                toc_lines.append(i)
                toc_lines_cur_number += 1
                flag_new_line = False

    print_toc_lines = False
    if print_toc_lines:
        print('------------')
        for i in toc_lines:
            print(i['bbox'], parse_line(i['text']))
        print('-----------')

    return is_toc_page(toc_lines)


def is_toc_page(table):
    toc_with_pos = []

    total = len(table)

    for i in table:
        s, n, f = parse_line(i['text'])
        if f is True:
            # fix line like: (xii   Doc Ref # IHD-OS-KBL-Vol 12-1', 17")
            if match_string(s, 'Doc Ref') == -1 and match_string(s, 'Doc  Ref') == -1:
                toc_with_pos.append([i['bbox'], s, n])

    count = len(toc_with_pos)

    if total > 0 and float(count) / total > 0.3:
        return True, toc_with_pos
    else:
        return False, []

def update_toc_page(doc, i, table):
    '''
    update links in the same page
    :return:
    '''
    pass
    page = doc.loadPage(i)
    hylinks = get_links(page)

    for i in hylinks:
        for j in table:
            # if i['pos'].intersect(j['pos']):
            #    print("True: ", j['label'],i['page'])
            if match(i['pos'], j[0]):
                debug_update_toc_page = False
                if debug_update_toc_page:
                    print("compare: ", j[0][0], i['page'], i['pos'], j[1], j[0], )
                    j.append(i['page'])
                else:
                    j[2] = i['page']
                break

def update_toc_levels(table):
    '''
    update levels in all pages
    :return:
    '''
    pass
    l = [r[0][0] for r in table]
    s = sorted(set(l))

    for j, vv in enumerate(l):
        for k, v in enumerate(s):
            if vv == v:
                l[j] = vv - v + k + 1
                table[j][0] = int(l[j])
                break

def update_toc_levels_2(table):
    '''
    update levels in all pages
    :return:
    '''

    old_lev = 0
    old_off = -1.0

    for j, vv in enumerate(table):
        new_lev = 1
        if table[j][0][0] > old_off:
            new_lev = int(old_lev + 1)
        elif table[j][0][0] < old_off:
            new_lev = int(old_lev - 1)
        else:
            new_lev = int(old_lev)

        # table[j][0] = int(old_lev)
        old_off = table[j][0][0]
        table[j][0] = new_lev
        old_lev = new_lev

def check_toc_level(toc, flag=False):
    mod = False
    toclen = len(toc)
    for i in list(range(toclen-1)):
        t1 = toc[i]
        t2 = toc[i+1]
        # if not -1 <= t1[2] <= pageCount:
        #     raise ValueError("row %s:page number out of range" % (str(i),))
        if (type(t2) is not list) or len(t2) < 3 or len(t2) > 4:
            print("arg2 must contain lists of 3 or 4 items")
        if (type(t2[0]) is not int) or t2[0] < 1:
            print("hierarchy levels must be int > 0")
        if t2[0] > t1[0] + 1:
            print("row {} ({}): hierarchy steps must not be > 1".format(i, toc[i]))
            if flag ==True:
                print("EEEEEE")
                break

            offset = t2[0] - t1[0]

            for j in list(range(i+2, toclen-1)):
                ''' process sub items'''
                if toc[j][0] < toc[i+1][0]:
                    break
                print("original {}: ".format(toc[j][0]))
                toc[j][0] -= offset
                print("modified {}: ".format(toc[j][0]))

            toc[i+1][0] -= offset
            mod = True
    return mod

    # no formal errors in toc --------------------------------------------------

#page = doc.loadPage(2)


#gen_toc(page)
#update_level()

# for i in g_toc:
#     print(i)

#update_level()





if __name__ == '__main__':
    # doc = fitz.open(r"C:\mybook\Dropbox\books\hw\intellinuxgraphics.org\010_kbl_-_2016-2017\intel-gfx-prm-osrc-kbl-vol02c-commandreference-registers-part1.pdf")
    # doc = fitz.open(r"C:\mybook\Dropbox\books\hw\intellinuxgraphics.org\010_kbl_-_2016-2017\intel-gfx-prm-osrc-kbl-vol12-display.pdf")
    mydir = r"C:\mybook\Dropbox\books\hw\intellinuxgraphics.org\010_kbl_-_2016-2017"
    files = [
        "intel-gfx-prm-osrc-kbl-vol01-preface.pdf",
        "intel-gfx-prm-osrc-kbl-vol02a-commandreference-instructions.pdf",
        "intel-gfx-prm-osrc-kbl-vol02b-commandreference-enumerations.pdf",
        "intel-gfx-prm-osrc-kbl-vol02c-commandreference-registers-part1.pdf",
        "intel-gfx-prm-osrc-kbl-vol02c-commandreference-registers-part2.pdf",
        "intel-gfx-prm-osrc-kbl-vol02d-commandreference-structures.pdf",
        "intel-gfx-prm-osrc-kbl-vol03-gpu_overview.pdf",
        "intel-gfx-prm-osrc-kbl-vol04-configurations.pdf",
        "intel-gfx-prm-osrc-kbl-vol05-memory_views.pdf",
        "intel-gfx-prm-osrc-kbl-vol06-command_stream_programming.pdf",
        "intel-gfx-prm-osrc-kbl-vol07-3d_media_gpgpu.pdf",
        "intel-gfx-prm-osrc-kbl-vol08-media_vdbox.pdf",
        "intel-gfx-prm-osrc-kbl-vol09-media_vebox.pdf",
        "intel-gfx-prm-osrc-kbl-vol10-hevc.pdf",
        "intel-gfx-prm-osrc-kbl-vol11-blitter.pdf",
        "intel-gfx-prm-osrc-kbl-vol12-display.pdf",
        "intel-gfx-prm-osrc-kbl-vol13-mmio.pdf",
        "intel-gfx-prm-osrc-kbl-vol14-observability.pdf",
        "intel-gfx-prm-osrc-kbl-vol15-sfc.pdf",
        "intel-gfx-prm-osrc-kbl-vol16-workarounds.pdf"
    ]

    doc = fitz.open(path.join(mydir, files[10]))
    print(doc)

    # print(td['blocks'])
    # doc.setToC(toc)
    # doc.save(doc.name, incremental=True)

    page_start = find_toc_start_page(doc)
    print("Toc start page: {}".format(page_start))

    do_show_lines()
