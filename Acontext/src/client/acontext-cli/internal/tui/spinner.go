package tui

import (
	"fmt"
	"time"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

// Spinner frames
var spinnerFrames = []string{"⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"}

// SpinnerModel is a bubbletea model for a spinner
type SpinnerModel struct {
	message   string
	frame     int
	done      bool
	err       error
	result    string
	quitting  bool
	startTime time.Time
}

// NewSpinner creates a new spinner model
func NewSpinner(message string) SpinnerModel {
	return SpinnerModel{
		message:   message,
		frame:     0,
		startTime: time.Now(),
	}
}

type spinnerTickMsg struct{}

func spinnerTick() tea.Cmd {
	return tea.Tick(80*time.Millisecond, func(time.Time) tea.Msg {
		return spinnerTickMsg{}
	})
}

// SpinnerDoneMsg signals the spinner to stop
type SpinnerDoneMsg struct {
	Err    error
	Result string
}

func (m SpinnerModel) Init() tea.Cmd {
	return spinnerTick()
}

func (m SpinnerModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "ctrl+c", "q":
			m.quitting = true
			return m, tea.Quit
		}
	case spinnerTickMsg:
		if m.done {
			return m, nil
		}
		m.frame = (m.frame + 1) % len(spinnerFrames)
		return m, spinnerTick()
	case SpinnerDoneMsg:
		m.done = true
		m.err = msg.Err
		m.result = msg.Result
		return m, tea.Quit
	}
	return m, nil
}

func (m SpinnerModel) View() string {
	if m.quitting {
		return ""
	}
	if m.done {
		if m.err != nil {
			return ErrorStyle.Render(IconError+" ") + m.message + " " + ErrorStyle.Render("failed")
		}
		if m.result != "" {
			return SuccessStyle.Render(IconSuccess+" ") + m.result
		}
		return SuccessStyle.Render(IconSuccess+" ") + m.message + " " + SuccessStyle.Render("done")
	}

	spinner := lipgloss.NewStyle().Foreground(ColorPrimary).Render(spinnerFrames[m.frame])
	return spinner + " " + m.message
}

// RunSpinner runs a spinner while executing a function
// Returns the result string and error from the function
func RunSpinner(message string, fn func() (string, error)) (string, error) {
	if !IsTTY() {
		// Fallback for non-TTY: just print message and run function
		fmt.Print(message + "... ")
		result, err := fn()
		if err != nil {
			fmt.Println(ErrorStyle.Render("failed"))
		} else {
			fmt.Println(SuccessStyle.Render("done"))
		}
		return result, err
	}

	m := NewSpinner(message)
	p := tea.NewProgram(m)

	// Run the function in a goroutine
	resultChan := make(chan struct {
		result string
		err    error
	}, 1)

	go func() {
		result, err := fn()
		resultChan <- struct {
			result string
			err    error
		}{result, err}
		p.Send(SpinnerDoneMsg{Err: err, Result: result})
	}()

	if _, err := p.Run(); err != nil {
		return "", fmt.Errorf("spinner error: %w", err)
	}

	// Get the result
	res := <-resultChan
	fmt.Println() // Print newline after spinner
	return res.result, res.err
}

// RunSpinnerSimple runs a spinner for a function that only returns an error
func RunSpinnerSimple(message string, fn func() error) error {
	_, err := RunSpinner(message, func() (string, error) {
		return "", fn()
	})
	return err
}
