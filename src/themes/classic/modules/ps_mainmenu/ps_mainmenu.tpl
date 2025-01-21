{assign var=_counter value=0}
{function name="menu" nodes=[] depth=0 parent=null}
  
      {if $nodes|count}
        <ul class="top-menu" {if $depth == 2}id="top-menu"{/if} data-depth="{$depth}">
          {foreach from=$nodes item=node}
            {if $node.label == 'Kategorie' || $node.label == $root_label || $depth > 1}
              <div class="mm-block-display-janek {if $depth == 2} mm-indent-block-janek {/if}">
                <li class="{$node.type}{if $node.current} current {/if}{if $depth === 3} deeplevel_janek {/if}" id="{$node.page_identifier}">
                {assign var=_counter value=$_counter+1}
                  {if $depth > 1}
                    <a
                      class="{if $depth >= 2}dropdown-item{/if}{if $depth === 2} dropdown-submenu{/if}"
                      href="{$node.url}" data-depth="{$depth}"
                      {if $node.open_in_new_window} target="_blank" {/if}
                    >
                      {if $node.children|count}
                        {* Cannot use page identifier as we can have the same page several times *}
                        {assign var=_expand_id value=10|mt_rand:100000}
                        <span class="float-xs-right hidden-md-up">
                          <span data-target="#top_sub_menu_{$_expand_id}" data-toggle="collapse" class="navbar-toggler collapse-icons">
                            <i class="material-icons add">&#xE313;</i>
                            <i class="material-icons remove">&#xE316;</i>
                          </span>
                        </span>
                      {/if}
                      {$node.label}
                    </a>
                  {/if}
                  {if $node.children|count}
                      {menu nodes=$node.children depth=$node.depth parent=$node}
                  {/if}
                </li>
              </div>
            {/if}
          {/foreach}
        </ul>
      {/if}
{/function}

<div class="menu js-top-menu position-static hidden-sm-down" id="_desktop_top_menu">
    {menu nodes=$menu.children root_label="Gadżety wg kategorii "}
    <div class="clearfix"></div>
</div>
<div class="menu js-top-menu position-static hidden-sm-down" id="_desktop_top_menu2">
    {menu nodes=$menu.children root_label="Gadżety wg tematyki "}
    <div class="clearfix"></div>
</div>
