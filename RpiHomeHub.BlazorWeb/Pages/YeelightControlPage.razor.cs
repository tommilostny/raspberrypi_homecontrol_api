using Microsoft.AspNetCore.Components;
using RpiHomeHub.BlazorWeb.Lights.Models;
using RpiHomeHub.BlazorWeb.Lights.Services;
using System.Threading.Tasks;

namespace RpiHomeHub.BlazorWeb.Pages
{
    public partial class YeelightControlPage : ComponentBase
    {
        [Inject]
        public YeelightService YeelightService { get; set; }

        private YeelightModel Yeelight { get; set; }

        protected override async Task OnInitializedAsync()
        {
            await Load();
            await base.OnInitializedAsync();
        }

        private async Task Load()
        {
            Yeelight = await YeelightService.GetStatusAsync();
        }
    }
}
