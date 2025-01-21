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
{block name='header_banner'}
  <div class="header-banner">
    {hook h='displayBanner'}
  </div>
{/block}

{block name='header_nav'}
  <nav class="header-nav">
    <div class="container">
      <div class="hidden-sm-down">
        {hook h='displayNav1'}
        
        <div class="col-md-7 right-nav">
        </div>
      </div>
      <div class="hidden-md-up text-sm-center mobile">
        <div class="float-xs-left" id="menu-icon">
          <i class="material-icons d-inline">&#xE5D2;</i>
        </div>
        <div class="float-xs-right" id="_mobile_cart"></div>
        <div class="float-xs-right" id="_mobile_user_info"></div>
        <div class="top-logo" id="_mobile_logo"></div>
        <div class="clearfix"></div>
      </div>
    </div>
  </nav>
{/block}

{block name='header_top'}
  <script src="https://kit.fontawesome.com/12c63f6a95.js" crossorigin="anonymous"></script>
  <div class="header-top">
    <div class="container">
       <div class="row">
        <div class="col-md-2 hidden-sm-down" id="_desktop_logo">
          {if $shop.logo_details}
            {if $page.page_name == 'index'}
              <h1>
                {renderLogo}
              </h1>
            {else}
              {renderLogo}
            {/if}
          {/if}
        </div>
        <div class="header-top-right col-md-10 col-sm-12 position-static">
          <div class="head-data-janek">
            <div class="infolinia-janek head-element-janek">
              Infolinia  <i class="fas fa-phone-square-alt"></i>  503 028 506
            </div>
            <div class="head-element-janek">
              Dostawa gratis od 250 zł
            </div>
            <div class="links-janek">
              <div class="head-element-janek">
                <a href="/content/14-bylem-tu">O nas</a>
              </div>
              <div class="head-element-janek">
                <a href="/content/14-bylem-tu">Regulamin</a>
              </div>
              <div class="head-element-janek">
                <a href="/content/14-bylem-tu">Dostawa</a>
              </div>
              <div class="head-element-janek">
                <a href="/kontakt">Kontakt</a>
              </div>
              <div class="head-element-janek">
                <a href="https://www.facebook.com/monsteriadapl">
                  <i class="fab fa-facebook-square"></i>
                </a>
                <a href="https://www.instagram.com/monsteriada/">
                  <i class="fab fa-instagram-square"></i>
                </a>
              </div>
            </div>
          </div>
          <div class="two-data-janek">
            {hook h="displayTop"}
            <div class="button_holder">
              {hook h='displayNav2'}
            </div>
          </div>
        </div>
      </div>
      <div id="mobile_top_menu_wrapper" class="row hidden-md-up" style="display:none;">
        <div class="js-top-menu mobile" id="_mobile_top_menu"></div>
        <div class="js-top-menu-bottom">
          <div id="_mobile_currency_selector"></div>
          <div id="_mobile_language_selector"></div>
          <div id="_mobile_contact_link"></div>
        </div>
      </div>
    </div>
  </div>
  
  <div class="main-navigation-janek">
    <a class="button-item" id="start-page-btn" href="/">Start</a>
    <a class="button-item category-items-button">
      Gadżety wg kategorii
      <i class="icon-arrow-down"></i>
    </a>
    <a class="button-item topic-items-button">
      Gadżety wg tematyki
      <i class="icon-arrow-down"></i>
    </a>
    <a class="button-item" href="/96-bestsellery">Bestsellery</a>
    <a class="button-item" href="/95-promocje">Promocje</a>
    <a class="button-item" href="/94-nowosci">Nowości</a>
    <a class="button-item" href="/content/14-bylem-tu">Blog</a>
  </div>
  <script>
    window.onload = function() {
      if (window.location.href === '/') {
        const button = document.getElementById('start-page-btn');
        if (button) {
          button.style.setProperty('color', '#cce963', 'important');
        } else {
          console.log('Element not found');
        }
      }
    };
  </script>
  {hook h='displayNavFullWidth'}
{/block}
