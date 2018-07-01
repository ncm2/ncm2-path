if get(s:, 'loaded', 0)
    finish
endif
let s:loaded = 1

let g:ncm2_path#proc = yarp#py3('ncm2_path')

let g:ncm2_path#source = get(g:, 'ncm2_path#source', {
            \ 'name': 'path',
            \ 'priority': 6,
            \ 'mark': '/',
            \ 'word_pattern': '([^\W]|[-.~%$])+',
            \ 'complete_pattern': [
            \       '(\.[/\\]+|[a-zA-Z]:\\+|~\/+)',
            \       '([^\W]|[-.~%$]|[/\\])+[/\\]+'],
            \ 'on_complete': 'ncm2_path#on_complete',
            \ 'on_warmup': 'ncm2_path#on_warmup',
            \ })

let g:ncm2_path#source = extend(g:ncm2_path#source,
            \ get(g:, 'ncm2_path#source_override', {}),
            \ 'force')

let g:ncm2_path#path_pattern = get(g:
            \ , 'ncm2_path#path_pattern', '(([^\W]|[-.~%$]|[/\\])+)')

func! ncm2_path#init()
    call ncm2#register_source(g:ncm2_path#source)
endfunc

func! ncm2_path#on_warmup(ctx)
    call g:ncm2_path#proc.jobstart()
endfunc

func! ncm2_path#on_complete(ctx)
    call g:ncm2_path#proc.try_notify('on_complete', a:ctx, g:ncm2_path#path_pattern)
endfunc

