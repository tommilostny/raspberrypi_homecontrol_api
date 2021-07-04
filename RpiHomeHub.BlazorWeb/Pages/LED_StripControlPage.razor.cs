using Microsoft.AspNetCore.Components;
using RpiHomeHub.BlazorWeb.Lights.Models;
using RpiHomeHub.BlazorWeb.Lights.Services;
using System.Threading.Tasks;

namespace RpiHomeHub.BlazorWeb.Pages
{
    public partial class LED_StripControlPage : ComponentBase
    {
        [Inject]
        public LED_StripService StripService { get; set; }

        private LED_StripModel Strip { get; set; }

        protected override async Task OnInitializedAsync()
        {
            await Load();
            await base.OnInitializedAsync();
        }

        private async Task Load()
        {
            Strip = await StripService.GetStatusAsync();
        }
    }
}
