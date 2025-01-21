{**
 * 2007-2020 PrestaShop SA and Contributors
 *
 * NOTICE OF LICENSE
 *
 * This source file is subject to the Academic Free License 3.0 (AFL-3.0)
 * that is bundled with this package in the file LICENSE.txt.
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
 * needs please refer to https://www.prestashop.com for more information.
 *
 * @author    PrestaShop SA <contact@prestashop.com>
 * @copyright 2007-2020 PrestaShop SA and Contributors
 * @license   https://opensource.org/licenses/AFL-3.0 Academic Free License 3.0 (AFL-3.0)
 * International Registered Trademark & Property of PrestaShop SA
 *}

<div id="search_widget" class="search-widgets" data-search-controller-url="{$search_controller_url}">
  <form method="get" action="{$search_controller_url}">
    <input type="text" name="s" value="{$search_string}" placeholder="{l s='Szukaj...' d='Shop.Theme.Catalog'}" aria-label="{l s='Search' d='Shop.Theme.Catalog'}">
    <input type="hidden" name="controller" value="search">
    <svg id="searcher" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="22" height="23"><path fill-rule="evenodd" d="M-0.007,21.318 C-0.007,21.511 0.061,21.676 0.196,21.812 C0.332,21.949 0.493,22.017 0.679,22.017 C0.865,22.017 1.029,21.945 1.172,21.801 L7.819,15.098 C9.435,16.502 11.307,17.204 13.437,17.204 C14.995,17.204 16.432,16.821 17.747,16.054 C19.062,15.288 20.102,14.247 20.867,12.929 C21.632,11.611 22.014,10.171 22.014,8.611 C22.014,7.049 21.632,5.610 20.867,4.292 C20.102,2.974 19.062,1.932 17.747,1.166 C16.432,0.400 14.999,0.016 13.448,0.016 C11.897,0.016 10.460,0.400 9.138,1.166 C7.816,1.932 6.772,2.974 6.007,4.292 C5.243,5.610 4.860,7.049 4.860,8.611 C4.860,10.687 5.525,12.521 6.854,14.110 L0.186,20.835 C0.057,20.964 -0.007,21.125 -0.007,21.318 ZM11.786,15.657 C11.243,15.528 10.735,15.345 10.264,15.110 C9.792,14.873 9.349,14.591 8.934,14.261 C8.520,13.931 8.148,13.555 7.819,13.132 C7.490,12.711 7.208,12.263 6.972,11.791 C6.736,11.317 6.554,10.809 6.425,10.264 C6.297,9.721 6.232,9.168 6.232,8.611 C6.232,7.307 6.554,6.100 7.197,4.990 C7.841,3.880 8.716,2.999 9.824,2.348 C10.932,1.696 12.140,1.370 13.448,1.370 C14.756,1.370 15.964,1.696 17.072,2.348 C18.180,2.999 19.055,3.880 19.698,4.990 C20.342,6.100 20.663,7.307 20.663,8.611 C20.663,9.914 20.342,11.121 19.698,12.231 C19.055,13.340 18.180,14.221 17.072,14.873 C15.964,15.525 14.752,15.850 13.437,15.850 C12.880,15.850 12.329,15.786 11.786,15.657 Z"></path></svg>
    <i class="material-icons clear" aria-hidden="true">clear</i>
  </form>
</div>
