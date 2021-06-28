using Microsoft.AspNetCore.Components;
using System.Threading.Tasks;

namespace RpiHomeHub.BlazorWeb.LCD
{
    public partial class LCD_Control : ComponentBase
    {
        [Inject]
        private LCD_Service LcdService { get; set; }

        [Parameter]
        public int LineWidth { get; set; } = 16;

        [Parameter]
        public int LinesCount { get; set; } = 2;

        protected override Task OnInitializedAsync()
        {
            LcdService.LineWidth = LineWidth;
            LcdService.LinesCount = LinesCount;
            return base.OnInitializedAsync();
        }

        private void MessageInput(ChangeEventArgs e)
        {
            LcdService.Message = e.Value.ToString();
        }
    }
}
