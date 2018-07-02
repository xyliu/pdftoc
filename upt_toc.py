import fitz
from os import path

from getlinks import find_toc_start_page, toc_in_page, update_toc_page, update_toc_levels, check_toc_level, \
    update_toc_levels_2

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


def add_toc_to_pdf(filename):
    doc = fitz.open(filename)
    page_start = find_toc_start_page(doc)
    page_id = [page_start, doc.pageCount]
    print(page_id)
    if page_id[0] <= 0:
        print("NO ToC found!\n")
        exit(-1)

    # ToC() of the doc
    # toc = doc.getToC()
    # toc =[[lvl1, title1, page1], [lvl2, title2, page2], ...]
    new_toc = []
    for i in range(page_id[0], page_id[1]):
        result, toc_i = toc_in_page(doc, i)
        if result is True:
            update_toc_page(doc, i, toc_i)
            new_toc += toc_i
            print_toc_i = False
            if print_toc_i:
                for i in toc_i:
                    print(i)
        else:
            break
    print_new_toc = False
    if print_new_toc:
        for i in new_toc:
            print(i)
    update_toc_levels(new_toc)

    #update_toc_levels_2(new_toc)

    print_new_toc = check_toc_level(new_toc)
    check_toc_level(new_toc, True)
    if print_new_toc:
        print(doc.name)
    print_new_toc= False
    if print_new_toc:
        for i in new_toc:
            print(i)
        print(doc.name)
    # doc.setToC(new_toc)
    # print(td['blocks'])


    # count = 0
    # refine =  check_toc_level(new_toc)
    # while refine:
    #     count += 1
    #     refine = check_toc_level()
    #
    #     if count >= 10:
    #         print("Too many faults")
    #         refine = False


    doc.setToC(new_toc)
    doc.save(doc.name, incremental=True)


if __name__ == '__main__':
    for i in files:
        #i = files[18]
        filename = path.join(mydir, i)
        add_toc_to_pdf(filename)
