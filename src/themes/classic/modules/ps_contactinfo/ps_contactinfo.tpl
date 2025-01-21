{**
 * Copyright since 2007 PrestaShop SA and Contributors
 * PrestaShop is an International Registered Trademark & Property of PrestaShop SA
 *
 * NOTICE OF LICENSE
 *
 * This source file is subject to the Academic Free License 3.0 (AFL-3.0)
 * that is bundled with this package in the file LICENSE.md.
 * It is also available through the world-wide-web at this URL:
 * https://opensource.org/licenses/AFL-3.0
 * If you did not receive a copy of the license and are unable to
 * obtain it through the world-wide-web, please send an email
 * to license@prestashop.com so we can send you a copy immediately.
 *
 * DISCLAIMER
 *
 * Do not edit or add to this file if you wish to upgrade PrestaShop to newer
 * versions in the future. If you wish to customize PrestaShop for your
 * needs please refer to https://devdocs.prestashop.com/ for more information.
 *
 * @author    PrestaShop SA and Contributors <contact@prestashop.com>
 * @copyright Since 2007 PrestaShop SA and Contributors
 * @license   https://opensource.org/licenses/AFL-3.0 Academic Free License 3.0 (AFL-3.0)
 *}

<div class="block-contact col-md-3 links wrapper">
  <div class="title clearfix hidden-md-up" data-target="#contact-infos" data-toggle="collapse">
    <span class="h3">{l s='Store information' d='Shop.Theme.Global'}</span>
    <span class="float-xs-right">
      <span class="navbar-toggler collapse-icons">
        <i class="material-icons add">keyboard_arrow_down</i>
        <i class="material-icons remove">keyboard_arrow_up</i>
      </span>
    </span>
  </div>

  <p class="h4 text-uppercase block-contact-title hidden-sm-down">Dane kontaktowe</p>
  <div id="contact-infos" class="collapse">
    <b>{$contact_infos.company}</b><br>
    {$contact_infos.address.address1}, {$contact_infos.address.address2}, {$contact_infos.address.city}
    {if $contact_infos.phone}
      <br>
      {* [1][/1] is for a HTML tag. *}
      <div id="janek-callus">
        {l s='Call us: [1]%phone%[/1]'
          sprintf=[
          '[1]' => '<div class="phone-number"><i class="fas fa-phone-square-alt"></i> ',
          '[/1]' => '</div>',
          '%phone%' => $contact_infos.phone
          ]
          d='Shop.Theme.Global'
        }
      </div>
    {/if}
    {if $contact_infos.fax}
      <br>
      {* [1][/1] is for a HTML tag. *}
      {l
        s='Fax: [1]%fax%[/1]'
        sprintf=[
          '[1]' => '<span>',
          '[/1]' => '</span>',
          '%fax%' => $contact_infos.fax
        ]
        d='Shop.Theme.Global'
      }
    {/if}
    {if $contact_infos.email && $display_email}
        Napisz wiadomość:<br>
        {mailto address=$contact_infos.email encode="javascript"}
    {/if}
    <div class="social-media-footer">
      <i class="fab fa-facebook-square" id="down-link-fb"></i>
      <i class="fab fa-instagram-square" id="down-link-ig"></i>
    </div>
  </div>
</div>
